# data_scraper.py
import praw
import tweepy
import pandas as pd
import time 
import random

# Reddit API setup
REDDIT_CLIENT_ID = "GbuL3ippfu12uomIBQCI2g"
REDDIT_CLIENT_SECRET = "I4fqPd_4or5crt50Lj9p9U4iOYzy5Q"
REDDIT_USER_AGENT = "GameBalanceAI/0.1 by Miju"
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

def scrape_reddit(subreddit="gaming", query="balance patch", limit=50):
    posts = []
    for post in reddit.subreddit(subreddit).search(query, limit=limit):
        posts.append({"source": "Reddit", "text": post.title + " " + post.selftext})
    return posts

# Twitter API setup
# TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABeLzwEAAAAA7Ox%2FTmDK4v5U2g2qtt6oiygVIwo%3DCJsrmcgqsSM8RmQuGU48xGQY7EmdxPM0JUYW0BAqHnmWPRRzEZ"
# client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# def scrape_twitter(keyword="game balance", limit=50):
#     tweets = []
#     response = client.search_recent_tweets(query=f"{keyword} -is:retweet lang:en", max_results=limit)
#     if response.data:
#         for tweet in response.data:
#             tweets.append({"source": "Twitter", "text": tweet.text})
#     return tweets