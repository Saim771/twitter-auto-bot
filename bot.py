# bot.py
import os
import random
import tweepy
import requests
from datetime import datetime

# Load environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate Twitter
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# 🔥 Function to generate AI-based tweet
def generate_ai_tweet():
    crypto_topics = [
        "Bitcoin", "Ethereum", "Crypto market", "Web3", "DeFi", "NFTs", "Blockchain"
    ]
    topic = random.choice(crypto_topics)
    # Use a public AI text generator API (free endpoint)
    prompt = f"Write a short, engaging, motivational tweet about {topic} with emojis and hashtags related to crypto."
    try:
        response = requests.get(
            f"https://api.monkedev.com/fun/chat?msg={prompt}"
        )
        data = response.json()
        ai_tweet = data.get("response", "Crypto never sleeps 🚀 #Bitcoin #Crypto")
    except:
        ai_tweet = "Crypto never sleeps 🚀 #Bitcoin #Crypto"
    return ai_tweet

# 🐦 Function to post tweet
def post_tweet():
    tweet_text = generate_ai_tweet()
    try:
        client.create_tweet(text=tweet_text)
        print(f"✅ Tweet posted: {tweet_text}")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")

# Run the bot
if __name__ == "__main__":
    post_tweet()
    
