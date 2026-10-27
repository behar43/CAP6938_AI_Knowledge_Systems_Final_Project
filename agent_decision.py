#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import json

from llm_client import ask_llm


#Ask the LLM whether to finish or investigate more restaurants.
def decide_next_action(
    preferences,
    ranked_restaurants,
    remaining_candidates,
    rounds_completed,
    max_rounds=3
):

    #Hard limits always take precedence over the LLM.
    if rounds_completed >= max_rounds:
        return {
            "action": "finish",
            "reason": "Maximum search rounds reached."
        }

    if remaining_candidates <= 0:
        return {
            "action": "finish",
            "reason": "No additional restaurant candidates remain."
        }

    #Only send concise evidence summaries to the decision model.
    summaries = []

    for restaurant in ranked_restaurants:

        preference_evidence = {}

        for preference in preferences:

            score = restaurant["scores"][preference]

            preference_evidence[preference] = {
                "score": score["score"],
                "evidence_count": score["evidence_count"]
            }

        summaries.append({
            "name": restaurant["name"],
            "overall_score": restaurant["overall_score"],
            "preference_evidence": preference_evidence
        })

    prompt = f"""
You are a restaurant recommendation agent.

The customer has these preferences:
{json.dumps(preferences)}

Restaurants analyzed so far:
{json.dumps(summaries, indent=2)}

Additional restaurant candidates available: {remaining_candidates}

Decide whether the agent should:
1. "finish" - present the current recommendations.
2. "search_more" - investigate additional restaurants.

Guidelines:
- Prefer investigating more restaurants when important preferences
  have negative evidence across the current recommendations.
- Consider searching more when evidence is insufficient.
- Do not assume that missing evidence means a preference is satisfied.
- Do not continue searching without a useful reason.
- Base the decision only on the provided evidence.

Return only a JSON object with this structure:
{{
    "action": "finish or search_more",
    "reason": "A short explanation"
}}
"""

    try:
        response = ask_llm(prompt, json_mode=True)
        decision = json.loads(response)

        if not isinstance(decision, dict):
            raise ValueError("Decision must be a JSON object.")

        action = decision.get("action")
        reason = decision.get("reason")

        if action not in ("finish", "search_more"):
            raise ValueError(f"Invalid agent action: {action}")

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Agent decision requires a reason.")

        return {
            "action": action,
            "reason": reason
        }

    except (ValueError, TypeError, KeyError) as error:

        #A malformed decision must not cause an unbounded loop.
        return {
            "action": "finish",
            "reason": f"Decision validation failed: {error}"
        }

