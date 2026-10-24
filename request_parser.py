#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import json
from llm_client import ask_llm

#Convert a natural-language restaurant request into structured criteria.
#Returns:
#    dict: Restaurant search constraints and customer preferences.
def parse_request(user_request):

    prompt = f"""
You are a restaurant search request parser.

Extract restaurant search constraints and customer preferences
from the user's request.

Return a JSON object with exactly these fields:

- cuisine: Restaurant cuisine as a string, or null if unspecified.
- min_stars: Minimum Yelp rating as a number, default 0.0.
- min_reviews: Minimum review count as an integer, default 0.
- preferences: List of customer preferences as short strings.

Rules:
- Extract only information provided by the user.
- Do not invent constraints or preferences.
- Keep preference descriptions short and meaningful.
- Do not place cuisine or minimum rating in preferences.
- Do not confuse the desired Yelp rating with a review's star rating.
- Return only a valid JSON object.
- Do not include explanations or Markdown.

User request:
{user_request}
"""

    response = ask_llm(prompt)

#    return json.loads(response)

    parsed = json.loads(response)
    
    if parsed.get("cuisine"):
        parsed["cuisine"] = parsed["cuisine"].strip()
    
    parsed["preferences"] = [
        preference.strip().lower()
        for preference in parsed["preferences"]
    ]
    
    return parsed
