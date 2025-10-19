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

# ------------------- API KEYS -------------------
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY")

# ------------------- TWITTER AUTH -------------------
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# ------------------- FLASK APP -------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Crypto Auto Tweet Bot Active: " + datetime.now(timezone.utc).isoformat()

# ------------------- PRICE FETCH FUNCTION -------------------
def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        res = requests.get(url, timeout=10).json()
        btc = res["bitcoin"]
        eth = res["ethereum"]
        sol = res["solana"]
        return f"💰 BTC: ${btc['usd']:,} ({btc['usd_24h_change']:.2f}%) | ETH: ${eth['usd']:,} ({eth['usd_24h_change']:.2f}%) | SOL: ${sol['usd']:,} ({sol['usd_24h_change']:.2f}%)"
    except Exception as e:
        print("⚠️ Error fetching prices:", e)
        return "💰 #Crypto market update"

# ------------------- NEWS FETCH FUNCTION -------------------
def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&filter=hot"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        posts = data.get("results", [])
        if not posts:
            return None
        post = random.choice(posts)
        title = post.get("title", "Crypto market update!")
        link = post.get("url", "")
        return f"🪙 {title}\n🔗 {link}"
    except Exception as e:
        print("❌ Error fetching news:", e)
        return None

# ------------------- POST TWEET FUNCTION -------------------
def post_tweet():
    try:
        news = get_crypto_news()
        prices = get_prices()
        if not news:
            print("⚠️ No news fetched.")
            return
        msg = f"{news}\n\n{prices}\n#Crypto #Bitcoin #Ethereum #Solana #Blockchain #AI"
        client.create_tweet(text=msg)
        print(f"✅ Tweeted at {datetime.now(timezone.utc).isoformat()}")
    except tweepy.errors.TooManyRequests:
        print("⏳ Rate limit reached, waiting 15 min...")
        time.sleep(900)
    except tweepy.errors.Forbidden as e:
        print("🚫 Forbidden:", e)
    except Exception as e:
        print("❌ Tweet error:", e)

# ------------------- MAIN LOOP -------------------
if __name__ == "__main__":
    print("🚀 Crypto Auto Bot started:", datetime.now(timezone.utc).isoformat())
    post_tweet()
    while True:
        time.sleep(3600)  # every 1 hour
        post_tweet()
