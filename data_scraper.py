# data_scraper.py
import praw
import tweepy
import pandas as pd
import time 
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABeLzwEAAAAA7Ox%2FTmDK4v5U2g2qtt6oiygVIwo%3DCJsrmcgqsSM8RmQuGU48xGQY7EmdxPM0JUYW0BAqHnmWPRRzEZ"
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

def scrape_twitter(keyword="game balance", limit=50):
    tweets = []
    response = client.search_recent_tweets(query=f"{keyword} -is:retweet lang:en", max_results=limit)
    if response.data:
        for tweet in response.data:
            tweets.append({"source": "Twitter", "text": tweet.text})
    return tweets

# OP.GG Scraping

def scrape_opgg():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.op.gg/champions"
    driver.get(url)
    time.sleep(3)  # Wait for JavaScript to load

    champion_data = []
    champion_elements = driver.find_elements(By.CSS_SELECTOR, ".css-1qq23jn .champion-box")

    for champion in champion_elements:
        name = champion.find_element(By.CSS_SELECTOR, ".css-1hyfx7x").text
        win_rate = champion.find_element(By.CSS_SELECTOR, ".css-1qk7wq1").text
        pick_rate = champion.find_element(By.CSS_SELECTOR, ".css-18d6k2n").text
        champion_data.append({"source": "OP.GG", "Champion": name, "Win Rate": win_rate, "Pick Rate": pick_rate})

    driver.quit()
    return champion_data