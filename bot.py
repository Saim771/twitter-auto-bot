import tweepy, os, time, random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def post_tweet():
    messages = [
        "🚀 Crypto never sleeps!",
        "💰 Stay bullish, stay focused!",
        "⚡ Every dip is a new opportunity!",
        "🌎 Web3 is the next internet revolution!"
    ]
    msg = random.choice(messages)
    api.update_status(msg)
    print(f"Tweeted: {msg}")

# Run daily
while True:
    post_tweet()
    time.sleep(86400)  # 24 hours
  
