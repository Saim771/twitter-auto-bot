# bot.py
import os
import random
import requests
import tweepy
from datetime import datetime, timezone
import time

# Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

# Authenticate using Tweepy v2 Client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic API"""
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&kind=news"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json().get("results", [])
            if not data:
                return "No crypto news found."
            post = random.choice(data)
            title = post.get("title", "No title")
            link = post.get("url", "")
            return f"📰 {title}\n🔗 {link}\n#Crypto #Bitcoin #AI"
        else:
            return f"⚠️ CryptoPanic error: {res.status_code}"
    except Exception as e:
        return f"❌ API error: {e}"

def post_tweet():
    """Post tweet using Twitter API v2"""
    msg = get_crypto_news()
    try:
        client.create_tweet(text=msg)
        print("✅ Tweet posted:", msg)
    except tweepy.Forbidden as e:
        print("⛔ Permission error (403):", e)
        print("⚠️ Check that your app has Read & Write access, then regenerate all keys/tokens.")
    except tweepy.TooManyRequests:
        print("⏳ Rate limit reached, waiting 15 min...")
        time.sleep(900)
    except Exception as e:
        print("❌ Error posting tweet:", e)

if __name__ == "__main__":
    print("Bot started:", datetime.now(timezone.utc).isoformat(), "UTC")
    post_tweet()
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Twitter Auto Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask).start()
    print("Bot started and Flask server running...")
    # Call your tweet posting function
    post_tweet()
