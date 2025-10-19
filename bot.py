# bot.py
import os
import time
import requests
import tweepy
import random
from flask import Flask
from datetime import datetime, timezone

# === ENVIRONMENT VARIABLES ===
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Your CryptoPanic API key (can be hardcoded or via Railway variable)
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "fbf4e6c85261e461803afc1c9c51d1112935fea3")

# === TWITTER AUTHENTICATION ===
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

try:
    user = api.verify_credentials()
    print(f"✅ Authenticated as: @{user.screen_name}")
except Exception as e:
    print("❌ Twitter Auth Error:", e)
    exit()

# === FLASK SERVER (for uptime ping) ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running smoothly ✅"

# === GLOBAL VARIABLES ===
last_posted_titles = []
backoff_minutes = 15
tweet_interval = 1800  # 30 minutes (safe limit)

# === FETCH LATEST CRYPTONEWS ===
def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&kind=news"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data.get("results", [])
    except Exception as e:
        print("⚠️ Error fetching news:", e)
        return []

# === POST TWEET ===
def post_tweet():
    global last_posted_titles

    news_list = get_crypto_news()
    if not news_list:
        print("⚠️ No news found.")
        return

    for news in news_list:
        title = news.get("title")
        url = news.get("url")

        if not title or title in last_posted_titles:
            continue

        tweet_text = f"📰 {title}\n\n🔗 Read more: {url}\n#Crypto #Blockchain #Web3"
        print(f"Attempting to post: {title}")

        try:
            api.update_status(tweet_text)
            print(f"✅ Tweet posted: {title}")
            last_posted_titles.append(title)
            if len(last_posted_titles) > 20:
                last_posted_titles = last_posted_titles[-10:]
            break  # Post one tweet per cycle
        except tweepy.errors.Forbidden as e:
            print("⛔ Forbidden error posting tweet:", e)
            print("⚠️ Check App permissions (Read & Write) and regenerate tokens.")
            break
        except tweepy.errors.TooManyRequests:
            print("⏳ Rate limit reached, waiting 15 min...")
            time.sleep(15 * 60)
            break
        except Exception as e:
            print("⚠️ Error posting tweet:", e)
            continue

# === MAIN LOOP ===
if __name__ == "__main__":
    print("Bot started:", datetime.now(timezone.utc).isoformat())

    # Start Flask in a separate thread
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    while True:
        post_tweet()
        print(f"🕒 Sleeping for {tweet_interval/60:.0f} min...\n")
        time.sleep(tweet_interval)
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Flask server ko alag thread me start kar do
threading.Thread(target=run_flask).start()
