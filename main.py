#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from data_loader import load_restaurants
from review_retrieval import load_reviews
from agent import find_restaurants, recommend_candidates


#Display the ranked restaurant recommendations.
def display_recommendations(result):

    print("\n" + "=" * 60)
    print("RESTAURANT RECOMMENDATIONS")
    print("=" * 60)

    print(f"\nCandidates found: {result['candidate_count']}")
    print(f"Eligible restaurants: {result['eligible_count']}")

    recommendations = result["recommendations"]

    if not recommendations:
        print("\nNo restaurants matched the request.")
        return

    for position, restaurant in enumerate(recommendations, start=1):

        print(f"\n{position}. {restaurant['name']}")
        print(f"   Yelp rating: {restaurant['stars']}")
        print(f"   Yelp review count: {restaurant['review_count']}")
        print(f"   Preference score: {restaurant['overall_score']:+.4f}")
        print(f"   Reviews analyzed: {restaurant['reviews_analyzed']}")

        print("\n   Preference evidence:")

        for preference, evidence in restaurant["scores"].items():

            score = evidence["score"]
            count = evidence["evidence_count"]

            if score is None:
                description = "Insufficient evidence"
            elif score > 0:
                description = "Positive"
            elif score < 0:
                description = "Negative"
            else:
                description = "Mixed"

            print(
                f"     {preference}: {description} "
                f"(score={score}, evidence={count})"
            )

    print("\n" + "=" * 60)


#Run the command-line restaurant recommendation application.
def main():

    print("=" * 60)
    print("YELP RESTAURANT RECOMMENDATION AGENT")
    print("=" * 60)

    print("\nLoading Yelp restaurant dataset...")

    restaurants = load_restaurants(
        "../Yelp_JSON/tampa_restaurants.json"
    )

    reviews_by_business = load_reviews(
        "../Yelp_JSON/tampa_restaurant_reviews.jsonl"
    )

    print(f"Loaded {len(restaurants)} restaurants.")
    print("Restaurant reviews loaded.")

    while True:

        print("\nEnter your restaurant request.")
        print("Type 'quit' to exit.")

        user_request = input("\n> ").strip()

        if user_request.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        if not user_request:
            continue

        try:

            print("\nInterpreting your request...")

            agent_result = find_restaurants(
                user_request,
                restaurants
            )

            if not agent_result["shortlist"]:
                print("\nNo eligible restaurants found.")
                continue

            print("\nAnalyzing restaurant reviews...")

            result = recommend_candidates(
                agent_result,
                reviews_by_business,
                review_limit=1
            )

            display_recommendations(result)

        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()

