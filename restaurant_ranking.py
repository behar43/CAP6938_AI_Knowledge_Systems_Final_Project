#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge


#Adjust a preference score based on available evidence.
def adjusted_preference_score(score, evidence_count, smoothing=3):

    if score is None or evidence_count <= 0:
        return 0.0

    return score * evidence_count / (evidence_count + smoothing)


#Rank restaurants using preference scores and evidence counts.
#Returns:
#    list: Restaurants ordered from highest to lowest adjusted score.
def rank_restaurants(restaurant_analyses, preferences, smoothing=3):

    if not preferences:
        raise ValueError("At least one preference is required for ranking.")

    ranked = []

    for restaurant in restaurant_analyses:

        adjusted_scores = {}

        for preference in preferences:

            result = restaurant["scores"][preference]

            adjusted_scores[preference] = adjusted_preference_score(
                result["score"],
                result["evidence_count"],
                smoothing=smoothing
            )

        overall_score = (
            sum(adjusted_scores.values()) / len(preferences)
        )

        ranked.append({
            **restaurant,
            "adjusted_scores": adjusted_scores,
            "overall_score": overall_score
        })

    ranked.sort(
        key=lambda restaurant: (
            restaurant["overall_score"],
            restaurant["stars"],
            restaurant["review_count"]
        ),
        reverse=True
    )

    return ranked

