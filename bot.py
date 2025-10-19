import tweepy, os, time, random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # new for v2 API

# Using Tweepy v2 client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def post_tweet():
    messages = [
        "🚀 Crypto never sleeps!",
        "💰 Stay bullish, stay focused!",
        "⚡ Every dip is a new opportunity!",
        "🌎 Web3 is the next internet revolution!"
    ]
    msg = random.choice(messages)
    client.create_tweet(text=msg)
    print(f"Tweeted: {msg}")

# Run once every 24 hours
while True:
    post_tweet()
    time.sleep(86400)