#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

#Search restaurants using structured criteria.
#Returns:
#    list: Matching restaurant records, sorted by rating.
def search_restaurants(restaurants, cuisine=None, min_stars=0.0, min_reviews=0):
    results = []

    for business in restaurants.values():

        # Check cuisine against Yelp business categories.
        if cuisine is not None:
            categories = [
                category.strip().lower()
                for category in (business.get("categories") or "").split(",")
            ]

            if cuisine.strip().lower() not in categories:
                continue

        # Check minimum star rating.
        if business.get("stars", 0) < min_stars:
            continue

        # Check minimum review count.
        if business.get("review_count", 0) < min_reviews:
            continue

        results.append(business)

    # Sort by rating, then review count, highest first.
    results.sort(
        key=lambda business: (
            business.get("stars", 0),
            business.get("review_count", 0)
        ),
        reverse=True
    )

    return results
