#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from request_parser import parse_request
from restaurant_search import search_restaurants
from restaurant_analysis import analyze_restaurant

#Interpret a customer request and select restaurant candidates.
#Returns:
#    dict: Parsed criteria, candidate counts, and shortlisted restaurants.
def find_restaurants(
    user_request,
    restaurants,
    min_evidence_reviews=50,
    shortlist_size=3
):
    # Interpret the customer's natural-language request.
    criteria = parse_request(user_request)

    # Search the Yelp dataset using the extracted constraints.
    candidates = search_restaurants(
        restaurants,
        cuisine=criteria["cuisine"],
        min_stars=criteria["min_stars"],
        min_reviews=criteria["min_reviews"]
    )

    # Apply the internal minimum review-count threshold.
    eligible = [
        business
        for business in candidates
        if business["review_count"] >= min_evidence_reviews
    ]

    # Select restaurants for deeper review analysis.
    shortlist = eligible[:shortlist_size]

    return {
        "request": user_request,
        "criteria": criteria,
        "candidate_count": len(candidates),
        "eligible_count": len(eligible),
        "shortlist": shortlist
    }

#Analyze shortlisted restaurants against customer preferences.
#Returns:
#    list: Restaurant analyses containing review evidence and scores.
def analyze_candidates(
    agent_result,
    reviews_by_business,
    review_limit=2
):
    preferences = agent_result["criteria"]["preferences"]
    results = []

    for business in agent_result["shortlist"]:

        analysis = analyze_restaurant(
            business,
            reviews_by_business,
            preferences,
            review_limit=review_limit
        )

        results.append(analysis)

    return results
