# topic_modelling.py
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation

def extract_topics(text_data, num_topics=5):
    vectorizer = CountVectorizer(stop_words='english')
    transformed_data = vectorizer.fit_transform(text_data)
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(transformed_data)
    return lda_model, vectorizer
#hello