#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from review_retrieval import search_reviews
from review_analysis import analyze_review_by_preference
from evidence_aggregation import aggregate_evidence
from restaurant_scoring import score_restaurant

#Analyze a restaurant using retrieved reviews and the local LLM.
#Returns:
#    dict: Restaurant information, review evidence, and preference scores.
def analyze_restaurant(
    business,
    reviews_by_business,
    preferences,
    review_limit=5
):
    business_id = business["business_id"]

    # Retrieve reviews relevant to the customer's preferences.
    reviews = search_reviews(
        reviews_by_business,
        business_id,
        preferences,
        limit=review_limit
    )

    review_analyses = []

    # Analyze each retrieved review using Qwen3.
    for review in reviews:
        results = analyze_review_by_preference(
            review["text"],
            preferences
        )

        review_analyses.append({
            "review_id": review["review_id"],
            "stars": review["stars"],
            "date": review["date"],
            "results": results
        })

    # Aggregate the classifications from all analyzed reviews.
    summary = aggregate_evidence(review_analyses)

    # Calculate scores for each customer preference.
    scores = score_restaurant(summary)

    return {
        "business_id": business_id,
        "name": business["name"],
        "stars": business["stars"],
        "review_count": business["review_count"],
        "reviews_analyzed": len(review_analyses),
        "review_analyses": review_analyses,
        "evidence_summary": summary,
        "scores": scores
    }

