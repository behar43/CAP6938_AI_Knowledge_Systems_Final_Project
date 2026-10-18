#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import json
from pathlib import Path

# Default location of the Tampa restaurant reviews.
DATA_DIR = Path(__file__).resolve().parent.parent / "Yelp_JSON"

REVIEW_FILE = DATA_DIR / "tampa_restaurant_reviews.jsonl"

#Load reviews and organize them by business_id.
#Returns:
#    dict: Lists of reviews indexed by business_id.
def load_reviews(file_path=REVIEW_FILE):
    reviews_by_business = {}

    with Path(file_path).open("r", encoding="utf-8") as f:
        for line in f:
            review = json.loads(line)
            business_id = review["business_id"]

            if business_id not in reviews_by_business:
                reviews_by_business[business_id] = []

            reviews_by_business[business_id].append(review)

    return reviews_by_business

#Retrieve all reviews for a particular restaurant.
#Returns an empty list if the restaurant has no reviews.
def get_reviews(reviews_by_business, business_id):
    return reviews_by_business.get(business_id, [])

#Search reviews for keywords related to customer preferences.
#Returns matching reviews sorted by number of keyword matches.
def search_reviews(reviews_by_business, business_id, keywords, limit=10):
    reviews = get_reviews(reviews_by_business, business_id)
    results = []

    # Normalize keywords for case-insensitive matching.
    keywords = [keyword.strip().lower() for keyword in keywords if keyword.strip()]

    for review in reviews:
        text = review.get("text", "").lower()

        # Count how many different keywords appear in the review.
        score = sum(1 for keyword in keywords if keyword in text)

        if score > 0:
            results.append((score, review))

    # Rank reviews by keyword matches, highest first.
    results.sort(key=lambda item: item[0], reverse=True)

    return [review for score, review in results[:limit]]
