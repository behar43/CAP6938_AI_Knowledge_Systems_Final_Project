#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from request_parser import parse_request
from restaurant_search import search_restaurants
from restaurant_analysis import analyze_restaurant
from semantic_retrieval import SemanticReviewSearch
from restaurant_ranking import rank_restaurants
from analysis_cache import make_cache_key, load_cached_analysis, save_cached_analysis
from agent_decision import decide_next_action

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
        "shortlist": shortlist,
        "eligible_candidates": eligible
    }

#Analyze shortlisted restaurants using semantic retrieval and caching.
def analyze_candidates(
    agent_result,
    reviews_by_business,
    review_limit=2,
    preference_queries=None
):

    preferences = agent_result["criteria"]["preferences"]

    if preference_queries is None:
        preference_queries = {
            preference: preference
            for preference in preferences
        }

    semantic_search = None
    results = []

    for business in agent_result["shortlist"]:

        cache_key = make_cache_key(
            business_id=business["business_id"],
            preferences=preferences,
            preference_queries=preference_queries,
            review_limit=review_limit
        )

        cached_analysis = load_cached_analysis(cache_key)

        if cached_analysis is not None:

            print(f"Cache hit: {business['name']}")
            results.append(cached_analysis)
            continue

        print(f"Analyzing: {business['name']}")

        #Only load the embedding model when an analysis is needed.
        if semantic_search is None:
            semantic_search = SemanticReviewSearch()

        analysis = analyze_restaurant(
            business,
            reviews_by_business,
            preferences,
            review_limit=review_limit,
            semantic_search=semantic_search,
            preference_queries=preference_queries
        )

        save_cached_analysis(cache_key, analysis)

        results.append(analysis)

    return results

#Analyze shortlisted restaurants using semantic review retrieval.
#Returns:
#    list: Restaurant analyses containing review evidence and scores.
def analyze_candidates_old(
    agent_result,
    reviews_by_business,
    review_limit=2,
    preference_queries=None
):
    preferences = agent_result["criteria"]["preferences"]

    #Load the embedding model once for all candidate restaurants.
    semantic_search = SemanticReviewSearch()

    results = []

    for business in agent_result["shortlist"]:

        analysis = analyze_restaurant(
            business,
            reviews_by_business,
            preferences,
            review_limit=review_limit,
            semantic_search=semantic_search,
            preference_queries=preference_queries
        )

        results.append(analysis)

    return results

#Generate ranked restaurant recommendations from an agent search result.
#Returns:
#    dict: Customer criteria, analyzed restaurants, and ranked recommendations.
def recommend_candidates(
    agent_result,
    reviews_by_business,
    review_limit=1,
    preference_queries=None
):
    preferences = agent_result["criteria"]["preferences"]

    analyses = analyze_candidates(
        agent_result,
        reviews_by_business,
        review_limit=review_limit,
        preference_queries=preference_queries
    )

    ranked = rank_restaurants(
        analyses,
        preferences
    )

    return {
        "request": agent_result["request"],
        "criteria": agent_result["criteria"],
        "candidate_count": agent_result["candidate_count"],
        "eligible_count": agent_result["eligible_count"],
        "recommendations": ranked
    }

#Run a bounded LLM-driven restaurant recommendation loop.
def run_agent(
    agent_result,
    reviews_by_business,
    review_limit=1,
    batch_size=3,
    max_rounds=3
):
    preferences = agent_result["criteria"]["preferences"]
    eligible = agent_result["eligible_candidates"]

    analyses = []
    decision_history = []
    next_index = 0

    for round_number in range(1, max_rounds + 1):

        #Select restaurants not previously analyzed.
        batch = eligible[next_index:next_index + batch_size]

        if not batch:
            break

        print(f"\nAgent round {round_number}")
        print(f"Analyzing {len(batch)} restaurants...")

        #Reuse our existing analysis function with a temporary shortlist.
        batch_result = {
            **agent_result,
            "shortlist": batch
        }

        batch_analyses = analyze_candidates(
            batch_result,
            reviews_by_business,
            review_limit=review_limit
        )

        analyses.extend(batch_analyses)
        next_index += len(batch)

        #Rank all restaurants analyzed so far.
        ranked = rank_restaurants(analyses, preferences)

        #Ask the LLM whether more investigation is necessary.
        decision = decide_next_action(
            preferences=preferences,
            ranked_restaurants=ranked,
            remaining_candidates=len(eligible) - next_index,
            rounds_completed=round_number,
            max_rounds=max_rounds
        )

        decision_history.append({
            "round": round_number,
            "action": decision["action"],
            "reason": decision["reason"]
        })

        print(f"Agent decision: {decision['action']}")
        print(f"Reason: {decision['reason']}")

        if decision["action"] == "finish":
            break

    return {
        "request": agent_result["request"],
        "criteria": agent_result["criteria"],
        "candidate_count": agent_result["candidate_count"],
        "eligible_count": agent_result["eligible_count"],
        "recommendations": ranked if analyses else [],
        "decision_history": decision_history,
        "restaurants_analyzed": len(analyses)
    }

