# bot.py
import tweepy
import os
import time
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Initialize Tweepy client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Function to post a tweet
def post_tweet():
    msg = "Hello World! This is my automated tweet."  # <-- Change your tweet content here
    try:
        client.create_tweet(text=msg)
        print("Tweet sent successfully!")
    except tweepy.errors.TooManyRequests:
        print("Rate limit reached. Waiting 1 hour before retry...")
        time.sleep(60*60)  # Wait 1 hour on rate limit
    except tweepy.errors.Forbidden as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

# Main loop to run the bot automatically
print("Bot started. Posting every 6 hours...")

while True:
    post_tweet()
    time.sleep(6*60*60)  # 6 hours delay; change to 24*60*60 for daily tweets
