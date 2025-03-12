# dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# 1) Import from your other files
from data_scraper import scrape_reddit, scrape_twitter, scrape_opgg
from sentiment_analysis import process_feedback

def generate_wordcloud(text_data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(text_data))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    st.title("Game Balance Sentiment Dashboard")
    st.subheader("Visualising balance concerns in games")

    # 2) Scrape data
    reddit_data = scrape_reddit()
    # twitter_data = scrape_twitter()
    opgg_data = scrape_opgg()
    feedback_data = reddit_data

    # 3) Process sentiment
    processed_data = process_feedback(feedback_data)

    # 4) Save data to CSV
    df = pd.DataFrame(processed_data)
    df.to_csv("sentiment_analysis_data.csv", index=False)
    st.success("Data and Sentiment Analysis saved as 'sentiment_analysis_data.csv'")

    # 5) Display data
    st.subheader("Collected Feedback Data")
    st.dataframe(df)

    # 6) Generate and display word cloud
    st.subheader("Word Cloud of Feedback")
    generate_wordcloud([entry['text'] for entry in processed_data])

if __name__ == "__main__":
    main()
