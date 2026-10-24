#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from review_retrieval import search_reviews, get_reviews
from review_analysis import analyze_review_by_preference
from evidence_aggregation import aggregate_evidence
from restaurant_scoring import score_restaurant
from review_analysis import analyze_reviews_batch


#Analyze restaurant reviews against customer preferences.
#Returns:
#    dict: Restaurant information, evidence summaries, and preference scores.
def analyze_restaurant(
    business,
    reviews_by_business,
    preferences,
    review_limit=5,
    semantic_search=None,
    preference_queries=None
):
    business_id = business["business_id"]

    if semantic_search is not None:

        reviews = get_reviews(reviews_by_business, business_id)
        semantic_search.build_index(reviews)

        if preference_queries is None:
            preference_queries = {
                preference: preference
                for preference in preferences
            }

        matches = semantic_search.search_preferences(
            preference_queries,
            limit_per_preference=review_limit
        )

        selected_reviews = [
            match["review"]
            for match in matches
        ]

    else:
        selected_reviews = search_reviews(
            reviews_by_business,
            business_id,
            preferences,
            limit=review_limit
        )

    #First version of review analysis
#    review_analyses = []
#
#    for review in selected_reviews:
#
#        results = analyze_review_by_preference(
#            review["text"],
#            preferences
#        )
#
#        review_analyses.append({
#            "review_id": review["review_id"],
#            "stars": review["stars"],
#            "date": review["date"],
#            "results": results
#        })

    #Classify the selected reviews in one LLM request.
    review_analyses = analyze_reviews_batch(
        selected_reviews,
        preferences
    )

    evidence_summary = aggregate_evidence(review_analyses)
    scores = score_restaurant(evidence_summary)

    return {
        "business_id": business_id,
        "name": business["name"],
        "stars": business["stars"],
        "review_count": business["review_count"],
        "reviews_analyzed": len(review_analyses),
        "review_analyses": review_analyses,
        "evidence_summary": evidence_summary,
        "scores": scores
    }

