from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return text

def tfidf_search(query, documents):
    """
    query: string (admin search query)
    documents: list of strings (skills + experience text)
    """
    cleaned_docs = [clean_text(doc) for doc in documents]
    cleaned_query = clean_text(query)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_docs + [cleaned_query])

    scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    return scores
