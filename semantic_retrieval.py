#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


#Build a semantic search index over Yelp reviews.
class SemanticReviewSearch:

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.reviews = []

    #Convert review text into normalized embeddings and build a FAISS index.
    def build_index(self, reviews):
        self.reviews = list(reviews)

        if not self.reviews:
            raise ValueError("Cannot build an index with no reviews.")

        texts = [review["text"] for review in self.reviews]

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        embeddings = np.asarray(embeddings, dtype=np.float32)

        dimension = embeddings.shape[1]

        # Inner product equals cosine similarity for normalized vectors.
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    #Retrieve reviews most similar to a natural-language query.
    #Returns:
    #    list: Matching reviews with their similarity scores.
    def search(self, query, limit=5):

        if self.index is None:
            raise ValueError("Build the review index before searching.")

        if limit <= 0:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(query_embedding, dtype=np.float32)

        k = min(limit, self.index.ntotal)

        similarities, indices = self.index.search(query_embedding, k)

        results = []

        for similarity, index in zip(similarities[0], indices[0]):
            results.append({
                "review": self.reviews[int(index)],
                "similarity": float(similarity)
            })

        return results

    #Retrieve reviews for multiple preferences and remove duplicates.
    #Returns:
    #    list: Unique reviews with similarity scores by preference.
    def search_preferences(self, queries, limit_per_preference=3):

        unique_reviews = {}

        for preference, query in queries.items():

            matches = self.search(query, limit=limit_per_preference)

            for match in matches:
                review = match["review"]
                review_id = review["review_id"]

                if review_id not in unique_reviews:
                    unique_reviews[review_id] = {
                        "review": review,
                        "similarities": {}
                    }

                unique_reviews[review_id]["similarities"][preference] = (
                    match["similarity"]
                )

        return list(unique_reviews.values())


