# sentiment_analysis.py
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return sia.polarity_scores(text)['compound']

def process_feedback(data):
    for entry in data:
        entry["sentiment"] = analyze_sentiment(entry["text"])
    return data