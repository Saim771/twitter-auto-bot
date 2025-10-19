# bot.py
import os
import random
import requests
import tweepy
from datetime import datetime, timezone
import time

# 🔑 Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CRYPTOPANIC_API_KEY = "fbf4e6c85261e461803afc1c9c51d1112935fea3"  # your real API key

# 🔧 Authenticate Twitter API (OAuth 1.0a)
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)
client = tweepy.API(auth)

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic API"""
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&kind=news"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            posts = data.get("results", [])
            if not posts:
                return "No latest crypto news right now."
            # Choose one random headline
            post = random.choice(posts)
            title = post.get("title", "No title available")
            link = post.get("url", "")
            return f"🪙 {title}\n🔗 {link}\n#Crypto #Bitcoin #AI"
        else:
            return f"⚠️ Error fetching news: {response.status_code}"
    except Exception as e:
        return f"❌ API error: {e}"

def post_tweet():
    """Post a crypto tweet"""
    msg = get_crypto_news()
    try:
        client.update_status(status=msg)
        print("✅ Tweet posted successfully:", msg)
    except tweepy.errors.TooManyRequests:
        print("⏳ Rate limit reached. Waiting 15 minutes...")
        time.sleep(900)
    except tweepy.errors.Forbidden as e:
        print("⛔ Forbidden error posting tweet:", e)
        print("⚠️ Check App permissions (Read & Write) and regenerate tokens.")
    except Exception as e:
        print("❌ Unexpected error posting tweet:", e)

if __name__ == "__main__":
    print("Bot started:", datetime.now(timezone.utc).isoformat(), "UTC")
    post_tweet()
