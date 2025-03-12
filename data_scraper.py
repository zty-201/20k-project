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
import json
import requests

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

CHAMPION_NAME_MAP = {
    "Aatrox": "Aatrox", "Ahri": "Ahri", "Akali": "Akali", "Akshan": "Akshan",
    "Alistar": "Alistar", "Amumu": "Amumu", "Anivia": "Anivia", "Annie": "Annie",
    "Aphelios": "Aphelios", "Ashe": "Ashe", "AurelionSol": "Aurelion Sol", "Azir": "Azir",
    "Bard": "Bard", "BelVeth": "Bel'Veth", "Blitzcrank": "Blitzcrank", "Brand": "Brand",
    "Braum": "Braum", "Caitlyn": "Caitlyn", "Camille": "Camille", "Cassiopeia": "Cassiopeia",
    "ChoGath": "Cho'Gath", "Corki": "Corki", "Darius": "Darius", "Diana": "Diana",
    "DrMundo": "Dr. Mundo", "Draven": "Draven", "Ekko": "Ekko", "Elise": "Elise",
    "Evelynn": "Evelynn", "Ezreal": "Ezreal", "Fiddlesticks": "Fiddlesticks", "Fiora": "Fiora",
    "Fizz": "Fizz", "Galio": "Galio", "Gangplank": "Gangplank", "Garen": "Garen",
    "Gnar": "Gnar", "Gragas": "Gragas", "Graves": "Graves", "Gwen": "Gwen",
    "Hecarim": "Hecarim", "Heimerdinger": "Heimerdinger", "Illaoi": "Illaoi", "Irelia": "Irelia",
    "Ivern": "Ivern", "Janna": "Janna", "JarvanIV": "Jarvan IV", "Jax": "Jax",
    "Jayce": "Jayce", "Jhin": "Jhin", "Jinx": "Jinx", "Kaisa": "Kai'Sa",
    "Kalista": "Kalista", "Karma": "Karma", "Karthus": "Karthus", "Kassadin": "Kassadin",
    "Katarina": "Katarina", "Kayle": "Kayle", "Kayn": "Kayn", "Kennen": "Kennen",
    "Khazix": "Kha'Zix", "Kindred": "Kindred", "Kled": "Kled", "KogMaw": "Kog'Maw",
    "KSante": "K'Sante", "Leblanc": "LeBlanc", "LeeSin": "Lee Sin", "Leona": "Leona",
    "Lillia": "Lillia", "Lissandra": "Lissandra", "Lucian": "Lucian", "Lulu": "Lulu",
    "Lux": "Lux", "Malphite": "Malphite", "Malzahar": "Malzahar", "Maokai": "Maokai",
    "MasterYi": "Master Yi", "Milio": "Milio", "MissFortune": "Miss Fortune", "Mordekaiser": "Mordekaiser",
    "Morgana": "Morgana", "Nami": "Nami", "Nasus": "Nasus", "Nautilus": "Nautilus",
    "Neeko": "Neeko", "Nidalee": "Nidalee", "Nilah": "Nilah", "Nocturne": "Nocturne",
    "Nunu": "Nunu & Willump", "Olaf": "Olaf", "Orianna": "Orianna", "Ornn": "Ornn",
    "Pantheon": "Pantheon", "Poppy": "Poppy", "Pyke": "Pyke", "Qiyana": "Qiyana",
    "Quinn": "Quinn", "Rakan": "Rakan", "Rammus": "Rammus", "RekSai": "Rek'Sai",
    "Rell": "Rell", "Renata": "Renata Glasc", "Renekton": "Renekton", "Rengar": "Rengar",
    "Riven": "Riven", "Rumble": "Rumble", "Ryze": "Ryze", "Samira": "Samira",
    "Sejuani": "Sejuani", "Senna": "Senna", "Seraphine": "Seraphine", "Sett": "Sett",
    "Shaco": "Shaco", "Shen": "Shen", "Shyvana": "Shyvana", "Singed": "Singed",
    "Sion": "Sion", "Sivir": "Sivir", "Skarner": "Skarner", "Sona": "Sona",
    "Soraka": "Soraka", "Swain": "Swain", "Sylas": "Sylas", "Syndra": "Syndra",
    "TahmKench": "Tahm Kench", "Taliyah": "Taliyah", "Talon": "Talon", "Taric": "Taric",
    "Teemo": "Teemo", "Thresh": "Thresh", "Tristana": "Tristana", "Trundle": "Trundle",
    "Tryndamere": "Tryndamere", "TwistedFate": "Twisted Fate", "Twitch": "Twitch", "Udyr": "Udyr",
    "Urgot": "Urgot", "Varus": "Varus", "Vayne": "Vayne", "Veigar": "Veigar",
    "VelKoz": "Vel'Koz", "Vex": "Vex", "Vi": "Vi", "Viego": "Viego",
    "Viktor": "Viktor", "Vladimir": "Vladimir", "Volibear": "Volibear", "Warwick": "Warwick",
    "Wukong": "Wukong", "Xayah": "Xayah", "Xerath": "Xerath", "XinZhao": "Xin Zhao",
    "Yasuo": "Yasuo", "Yone": "Yone", "Yorick": "Yorick", "Yuumi": "Yuumi",
    "Zac": "Zac", "Zed": "Zed", "Zeri": "Zeri", "Ziggs": "Ziggs",
    "Zilean": "Zilean", "Zoe": "Zoe", "Zyra": "Zyra"
}  

def scrape_opgg():
    url = "https://op.gg/api/v1.0/internal/bypass/meta/champions"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.op.gg/champions",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        champion_data = []
        for champ in data["data"]:
            champion_id = champ.get("key", "Unknown")
            name = CHAMPION_NAME_MAP.get(champion_id, champion_id)

            if "positionTierData" in champ and champ["positionTierData"]:
                win_rate = champ["positionTierData"][0].get("positionWinRate", "N/A")
                pick_rate = champ["positionTierData"][0].get("positionPickRate", "N/A")
            else:
                win_rate = "Unknown"
                pick_rate = "Unknown"

            text_description = f"{name} has a {win_rate}% win rate and a {pick_rate}% pick rate."

            champion_data.append({
                "source": "OP.GG",
                "text": text_description,
                "Champion": name,
                "Win Rate": win_rate,
                "Pick Rate": pick_rate
            })

        # print(f"✅ Found {len(champion_data)} champions from OP.GG API")
        return champion_data

    else:
        print(f"❌ Failed to fetch OP.GG data: {response.status_code}")
        return []