# data_scraper.py
import praw
import tweepy
import pandas as pd
import time 
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Reddit API setup
REDDIT_CLIENT_ID = "GbuL3ippfu12uomIBQCI2g"
REDDIT_CLIENT_SECRET = "I4fqPd_4or5crt50Lj9p9U4iOYzy5Q"
REDDIT_USER_AGENT = "GameBalanceAI/0.1 by Miju"
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

def scrape_reddit(subreddit="leagueoflegends", queries=None, limit=50):
    """
    Scrape Reddit posts based on categorized search queries
    
    Args:
        subreddit (str): Subreddit to search
        queries (dict): Dictionary where keys are categories and values are lists of queries
        limit (int): Maximum posts per query
        
    Returns:
        dict: Posts grouped by categories and flattened list
    """
    if queries is None:
        # Default categorized queries
        queries = {
            "General Balance Feedback": ["balance patch", "game balance"],
            "Patch-Specific Feedback": ["patch notes", "latest patch"],
            "Champion-Specific Issues": ["champion nerf", "champion buff", "overpowered"],
            "Pro Play Balance Impact": ["pro play balance", "esports balance"],
            "Role-Based Complaints": ["adc weak", "jungle diff", "support carry"]
        }
    
    categorized_posts = {category: [] for category in queries.keys()}
    total_posts = 0
    
    for category, query_list in queries.items():
        print(f"Collecting data for category: {category}")
        
        for query in query_list:
            try:
                print(f"  Searching r/{subreddit} for: '{query}'")
                query_count = 0
                
                for post in reddit.subreddit(subreddit).search(query, limit=limit):
                    post_data = {
                        "source": "Reddit",
                        "category": category,
                        "query": query,
                        "subreddit": subreddit,
                        "title": post.title,
                        "text": post.title + " " + post.selftext,
                        "score": post.score,
                        "url": f"https://reddit.com{post.permalink}",
                        "created_utc": post.created_utc
                    }
                    categorized_posts[category].append(post_data)
                    query_count += 1
                    total_posts += 1
                
                print(f"    Found {query_count} posts for query '{query}'")
                # Add a small delay between queries to avoid rate limiting
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"    Error searching for '{query}': {str(e)}")
    
    print(f"Total posts collected: {total_posts}")
    
    # Also return a flattened list for backward compatibility
    flattened_posts = [post for posts in categorized_posts.values() for post in posts]
    return categorized_posts, flattened_posts

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