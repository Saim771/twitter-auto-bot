# bot.py
import os
import time
import requests
import random
from flask import Flask
from datetime import datetime, timezone
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Load keys
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

# Twitter auth
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Flask web server (for uptime)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Crypto News Bot is running! " + datetime.now(timezone.utc).isoformat()

# Function to get latest crypto news
def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&filter=hot"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        posts = data.get("results", [])
        if not posts:
            return None
        post = random.choice(posts)
        title = post.get("title", "Crypto update!")
        link = post.get("url", "")
        return f"🪙 {title}\n🔗 {link}\n#Crypto #Bitcoin #Blockchain #AI"
    except Exception as e:
        print("❌ Error fetching news:", e)
        return None

# Function to post tweet
def post_tweet():
    try:
        msg = get_crypto_news()
        if not msg:
            print("⚠️ No news fetched.")
            return
        client.create_tweet(text=msg)
        print(f"✅ Tweet posted at {datetime.now(timezone.utc).isoformat()}: {msg}")
    except tweepy.errors.TooManyRequests:
        print("⏳ Rate limit reached, waiting 15 min...")
        time.sleep(900)
    except tweepy.errors.Forbidden as e:
        print("🚫 Forbidden:", e)
    except Exception as e:
        print("❌ Error posting tweet:", e)

if __name__ == "__main__":
    print("Bot started:", datetime.now(timezone.utc).isoformat(), "UTC")
    post_tweet()
    while True:
        time.sleep(3600)  # every 1 hour
        post_tweet()
