# data_scraper.py
import praw
import tweepy
import pandas as pd

# Reddit API setup
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "your_user_agent"
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

def scrape_reddit(subreddit="gaming", query="balance patch", limit=50):
    posts = []
    for post in reddit.subreddit(subreddit).search(query, limit=limit):
        posts.append({"source": "Reddit", "text": post.title + " " + post.selftext})
    return posts

# Twitter API setup
TWITTER_BEARER_TOKEN = "your_bearer_token"
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def scrape_twitter(keyword="game balance", limit=50):
    tweets = []
    response = client.search_recent_tweets(query=f"{keyword} -is:retweet lang:en", max_results=limit)
    if response.data:
        for tweet in response.data:
            tweets.append({"source": "Twitter", "text": tweet.text})
    return tweets