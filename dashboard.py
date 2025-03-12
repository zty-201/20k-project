# dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_wordcloud(text_data):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(text_data))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    st.title("Game Balance Sentiment Dashboard")
    st.subheader("Visualising balance concerns in games")
    feedback_data = scrape_reddit() + scrape_twitter()
    processed_data = process_feedback(feedback_data)
    st.dataframe(processed_data)
    generate_wordcloud([entry['text'] for entry in processed_data])

if __name__ == "__main__":
    main()