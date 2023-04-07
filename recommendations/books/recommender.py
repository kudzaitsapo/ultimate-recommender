# Start with imports
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

# constant declarations
MODEL_NAME = "models/books.npz"
DF_NAME = "dataset.csv"

BASE_DIR = Path(__file__).resolve().parent
data_file = BASE_DIR / "data/dataset.csv"


# utility function declarations
def get_vectors(df, model):

    # Creating a list for storing the vectors (description into vectors)
    # global word_embeddings
    word_embeddings = []

    # Reading the each book description
    for line in df["cleaned"]:
        avgword2vec = None
        count = 0
        for word in line.split():
            if word in list(model.wv.index_to_key):
                count += 1
                if avgword2vec is None:
                    avgword2vec = model.wv[word]
                else:
                    avgword2vec = avgword2vec + model.wv[word]

        if avgword2vec is not None:
            avgword2vec = avgword2vec / count

            word_embeddings.append(avgword2vec)

    return word_embeddings


def get_tfidf_vectors(df, model, tfidf_list, tfidf_feature):
    tfidf_vectors = []
    line = 0

    corpus = build_copus(df)

    # for each book description
    for desc in corpus:
        # Word vectors are of zero length (Used 300 dimensions)
        sent_vec = np.zeros(300)
        # num of words with a valid vector in the book description
        weight_sum = 0
        # for each word in the book description
        for word in desc:
            if word in list(model.wv.index_to_key) and word in tfidf_feature:
                vec = model.wv[word]
                tf_idf = tfidf_list[word] * (desc.count(word) / len(desc))
                sent_vec += vec * tf_idf
                weight_sum += tf_idf

        if weight_sum != 0:
            sent_vec /= weight_sum

        tfidf_vectors.append(sent_vec)
        line += 1

    return tfidf_vectors


def recommendations(title, df, model):

    # Calling the function vectors

    embeddings = get_vectors(df, model)

    # finding cosine similarity for the vectors

    cosine_similarities = cosine_similarity(embeddings, embeddings)

    # taking the title and book image link and store in new data frame called books
    books = df[["title", "image_link"]]
    # Reverse mapping of the index
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    book_indices = [i[0] for i in sim_scores]
    recommend = books.iloc[book_indices]
    return recommend


def build_copus(df):
    corpus = []
    for words in df["cleaned"]:
        corpus.append(words.split())

    return corpus


def recommend_tfdf(title, df, model):
    # Building TFIDF model and calculate TFIDF score
    tfidf = TfidfVectorizer(analyzer="word", ngram_range=(1, 3), min_df=5, stop_words="english")
    tfidf.fit(df["cleaned"])

    # Getting the words from the TF-IDF model

    tfidf_list = dict(zip(tfidf.get_feature_names_out(), list(tfidf.idf_)))
    tfidf_feature = tfidf.get_feature_names_out()  # tfidf words/col-names

    # Building TF-IDF Word2Vec

    # Storing the TFIDF Word2Vec embeddings
    tfidf_vectors = get_tfidf_vectors(df, model, tfidf_list, tfidf_feature)

    # finding cosine similarity for the vectors

    cosine_similarities = cosine_similarity(tfidf_vectors, tfidf_vectors)

    # taking the title and book image link and store in new data frame called books
    books = df[["title", "image_link"]]
    # Reverse mapping of the index
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    book_indices = [i[0] for i in sim_scores]
    recommend = books.iloc[book_indices]

    return recommend


def recommend_book(title):
    model = Word2Vec.load(MODEL_NAME)
    dataframe = pd.read_csv(DF_NAME)
    return recommend_tfdf(title, dataframe, model)
