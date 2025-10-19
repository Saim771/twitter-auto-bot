import os
import time
import tweepy
import random
import requests

# --- Twitter API keys (from .env) ---
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# --- Tweepy client setup ---
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# --- Function to get fresh crypto news ---
def get_crypto_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        response = requests.get(url)
        data = response.json()

        articles = data["Data"]
        random_article = random.choice(articles)
        title = random_article["title"]
        source = random_article["source"]
        link = random_article["url"]

        tweet = f"📰 {title}\nSource: {source}\n#CryptoNews {link}"
        return tweet[:280]  # limit to 280 characters
    except Exception as e:
        print("❌ Error fetching news:", e)
        return None

# --- Post Tweet Function ---
def post_tweet():
    try:
        msg = get_crypto_news()
        if msg:
            client.create_tweet(text=msg)
            print(f"✅ Tweet posted:\n{msg}")
        else:
            print("⚠️ No tweet generated.")
    except tweepy.errors.TooManyRequests:
        print("⚠️ Rate limit reached — waiting 1 hour...")
        time.sleep(3600)
    except Exception as e:
        print("❌ Error posting tweet:", e)

# --- Auto loop: post every 6 hours ---
while True:
    post_tweet()
    time.sleep(6 * 60 * 60)  # 6 hours delay
