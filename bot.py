# bot.py
import os
import time
import random
import requests
import tweepy
from datetime import datetime

# ---------------------------
# CONFIG / ENV
# ---------------------------
# Twitter credentials: put these in Railway env variables (recommended)
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# CryptoPanic API key:
# Recommended: set as env var CRYPTOPANIC_API_KEY
# Fallback to the token you provided (for convenience). Replace later with env var for security.
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "fbf4e6c85261e461803afc1c9c51d1112935fea3")

# Posting interval (seconds) — default 6 hours
POST_INTERVAL_SECONDS = 6 * 60 * 60

# Max tweet length safety margin
TWEET_MAX = 280
TWEET_TRIM = 270

# ---------------------------
# Validate required creds
# ---------------------------
missing = []
for name, val in [
    ("API_KEY", API_KEY),
    ("API_SECRET_KEY", API_SECRET_KEY),
    ("ACCESS_TOKEN", ACCESS_TOKEN),
    ("ACCESS_TOKEN_SECRET", ACCESS_TOKEN_SECRET),
]:
    if not val:
        missing.append(name)

if missing:
    print("ERROR: Missing Twitter credentials in environment variables:", missing)
    print("Please add them in Railway Variables or .env and redeploy.")
    raise SystemExit(1)

# ---------------------------
# Twitter auth (OAuth1) using tweepy v4
# ---------------------------
try:
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # quick verify (safe)
    try:
        me = api.verify_credentials()
        print(f"Authenticated as: @{me.screen_name}")
    except Exception as e:
        print("Warning: verify_credentials failed:", e)
except Exception as e:
    print("Failed initializing Twitter client:", e)
    raise

# ---------------------------
# Helper: fetch crypto news from CryptoPanic
# ---------------------------
def get_crypto_news():
    """
    Returns a short tweet string from CryptoPanic latest/important posts.
    Uses CRYPTOPANIC_API_KEY. Returns None on failure.
    """
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&filter=important"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # CryptoPanic response structure may vary — handle common keys
        posts = data.get("results") or data.get("results") or data.get("posts") or data.get("data") or data.get("results")
        if not posts:
            # try other names / or fallback to top-level list
            # some responses use "results" or "results"
            posts = data.get("results") if isinstance(data.get("results"), list) else None

        if not posts:
            # fallback: try to parse whatever structure exists
            # if data has 'results' field or 'results' already checked, otherwise fail gracefully
            print("No posts array found in CryptoPanic response; returning fallback message.")
            return f"Crypto market never sleeps 🚀 #Crypto #Bitcoin"

        # Choose a post that has title+url
        chosen = None
        for _ in range(5):
            candidate = random.choice(posts)
            title = candidate.get("title") or candidate.get("domain_title") or candidate.get("kind")
            url_post = candidate.get("url") or candidate.get("link") or candidate.get("source_url") or ""
            if title:
                chosen = (title, url_post)
                break
        if not chosen:
            # pick first with any text
            candidate = posts[0]
            title = candidate.get("title") or "Crypto update"
            url_post = candidate.get("url") or ""
            chosen = (title, url_post)

        title, link = chosen
        # Build tweet content
        if link:
            tweet = f"📰 {title}\nRead: {link}\n#Crypto #CryptoNews"
        else:
            tweet = f"📰 {title}\n#Crypto #CryptoNews"

        # Trim to safe length
        if len(tweet) > TWEET_TRIM:
            tweet = tweet[:TWEET_TRIM].rsplit(" ", 1)[0] + "…"

        return tweet
    except requests.exceptions.RequestException as e:
        print("Network error fetching CryptoPanic:", e)
        return None
    except Exception as e:
        print("Error parsing CryptoPanic response:", e)
        return None

# ---------------------------
# Post tweet with robust error handling
# ---------------------------
def post_tweet():
    tweet_text = get_crypto_news()
    if not tweet_text:
        print("No tweet text generated; skipping this round.")
        return False

    try:
        status = api.update_status(status=tweet_text)
        print(f"✅ Tweet posted (id={getattr(status, 'id', 'unknown')}): {tweet_text}")
        return True
    except tweepy.errors.TooManyRequests as e:
        # Rate limited — backoff
        print("⚠️ TooManyRequests (429) from Twitter. Backing off.")
        return "rate_limited"
    except tweepy.errors.Forbidden as e:
        print("⛔ Forbidden error posting tweet:", e)
        # Could be permissions issue — stop further posting until fixed
        return "forbidden"
    except Exception as e:
        print("❌ Unexpected error posting tweet:", e)
        return False

# ---------------------------
# Main loop with backoff & jitter
# ---------------------------
def main_loop():
    from datetime import datetime, timezone
        print("Bot started:", datetime.now(timezone.utc).isoformat(), "UTC")
    backoff_hours = 1  # starting backoff on 429
    while True:
        try:
            result = post_tweet()
            if result == "rate_limited":
                # Wait exponential backoff (cap at 6 hours)
                wait = min(backoff_hours, 6) * 60 * 60
                print(f"Waiting for {wait/3600:.1f} hours due to rate limit.")
                time.sleep(wait)
                backoff_hours = min(backoff_hours * 2, 6)
                continue
            if result == "forbidden":
                print("Permissions error (Forbidden). Please check App permissions (Read & Write) and regenerate tokens. Exiting.")
                break
            # successful or skipped, reset backoff
            backoff_hours = 1

            # Sleep until next scheduled post, add small random jitter (0-10 minutes) to avoid simultaneous jobs
            jitter_seconds = random.randint(0, 10 * 60)
            total_sleep = POST_INTERVAL_SECONDS + jitter_seconds
            next_time = datetime.utcnow() + (time.timedelta(seconds=total_sleep) if hasattr(time, 'timedelta') else None)
            print(f"Next post in {total_sleep/3600:.2f} hours (including jitter).")
            time.sleep(total_sleep)
        except KeyboardInterrupt:
            print("Stopping on KeyboardInterrupt.")
            break
        except Exception as e:
            print("Unexpected error in main loop:", e)
            # small wait then continue
            time.sleep(60)

if __name__ == "__main__":
    main_loop()
