# dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import numpy as np

# 1) Import from your other files
from data_scraper import scrape_reddit, scrape_twitter, scrape_opgg
from sentiment_analysis import process_feedback, analyze_sentiment
from topic_modelling import extract_topics

def generate_wordcloud(text_data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(text_data))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def display_category_sentiment(categorized_data):
    """
    Display sentiment analysis by category
    """
    # Process sentiment for each category
    category_sentiments = {}
    
    for category, posts in categorized_data.items():
        if posts:
            # Process sentiment for each post in the category
            sentiments = []
            for post in posts:
                sentiment = analyze_sentiment(post['text'])
                sentiments.append(sentiment)
            
            # Calculate average sentiment
            avg_sentiment = sum(sentiments) / len(sentiments)
            category_sentiments[category] = avg_sentiment
    
    # Create a bar chart of category sentiments
    categories = list(category_sentiments.keys())
    sentiments = list(category_sentiments.values())
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(categories, sentiments)
    
    # Color bars based on sentiment (red for negative, green for positive)
    for i, sentiment in enumerate(sentiments):
        bars[i].set_color('green' if sentiment > 0 else 'red')
    
    ax.set_ylabel('Sentiment Score')
    ax.set_title('Average Sentiment by Discussion Category')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig

def main():
    st.title("Game Balance Sentiment Dashboard")
    st.subheader("Visualising balance concerns in games")

    # Sidebar configuration
    st.sidebar.title("Data Collection Settings")
    use_categories = st.sidebar.checkbox("Use categorized Reddit queries", value=True)
    
    # 2) Scrape data
    with st.spinner("Collecting data from Reddit..."):
        if use_categories:
            # Define your categories and queries
            custom_queries = {
                "General Balance Feedback": ["balance issues", "game balance"],
                "Patch-Specific Feedback": ["patch notes", "recent patch"],
                "Champion-Specific Issues": ["champion op", "champion nerf", "champion buff"],
                "Pro Play Balance Impact": ["pro play meta", "worlds balance"],
                "Role-Based Complaints": ["jungle difference", "adc weak", "support carry"]
            }
            
            categorized_data, reddit_data = scrape_reddit(
                subreddit="leagueoflegends",
                queries=custom_queries,
                limit=10
            )
        else:
            reddit_data = scrape_reddit()
            categorized_data = {"All Posts": reddit_data}
    
    # Optionally collect OP.GG data
    collect_opgg = st.sidebar.checkbox("Collect OP.GG champion data", value=False)
    if collect_opgg:
        with st.spinner("Collecting data from OP.GG..."):
            opgg_data = scrape_opgg()
            st.subheader("OP.GG Champion Data")
            st.dataframe(pd.DataFrame(opgg_data))

    # 3) Process sentiment
    processed_data = process_feedback(reddit_data)

    # 4) Save data to CSV
    df = pd.DataFrame(processed_data)
    df.to_csv("sentiment_analysis_data.csv", index=False)
    st.success("Data and Sentiment Analysis saved as 'sentiment_analysis_data.csv'")

    # 5) Display data
    st.subheader("Collected Feedback Data")
    st.dataframe(df)
    
    # 6) Display category-based sentiment if using categories
    if use_categories:
        st.subheader("Sentiment Analysis by Category")
        category_fig = display_category_sentiment(categorized_data)
        st.pyplot(category_fig)
        
        # Generate wordclouds for each category
        st.subheader("Word Clouds by Category")
        for category, posts in categorized_data.items():
            if posts:
                st.write(f"### {category}")
                category_texts = [post['text'] for post in posts]
                wc_fig = generate_wordcloud(category_texts)
                st.pyplot(wc_fig)
    else:
        # 7) Generate and display overall word cloud
        st.subheader("Word Cloud of All Feedback")
        wc_fig = generate_wordcloud([entry['text'] for entry in processed_data])
        st.pyplot(wc_fig)

if __name__ == "__main__":
    main()