#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from restaurant_search import search_restaurants
from review_retrieval import search_reviews

#Combine structured restaurant filtering with review retrieval.
#Returns:
#    list: Restaurant candidates with relevant review evidence.
def recommend_restaurants(
    restaurants,
    reviews_by_business,
    cuisine=None,
    min_stars=0.0,
    min_reviews=0,
    keywords=None,
    limit=5,
    reviews_per_restaurant=3
):
    if keywords is None:
        keywords = []

    # Find restaurants satisfying the structured requirements.
    candidates = search_restaurants(
        restaurants,
        cuisine=cuisine,
        min_stars=min_stars,
        min_reviews=min_reviews
    )

    recommendations = []

    for business in candidates:
        business_id = business["business_id"]

        # Retrieve reviews relevant to the customer's preferences.
        relevant_reviews = search_reviews(
            reviews_by_business,
            business_id,
            keywords,
            limit=reviews_per_restaurant
        ) if keywords else []

        # If keywords were requested, require at least one matching review.
        if keywords and not relevant_reviews:
            continue

        recommendations.append({
            "business_id": business_id,
            "name": business["name"],
            "stars": business["stars"],
            "review_count": business["review_count"],
            "categories": business["categories"],
            "reviews": relevant_reviews
        })

        if len(recommendations) >= limit:
            break

    return recommendations
