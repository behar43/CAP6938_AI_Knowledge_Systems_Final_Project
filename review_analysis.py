#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from llm_client import ask_llm
import json

#Analyze whether a Yelp review supports a customer's preferences.
#Returns:
#    str: The LLM's assessment of the review.
def analyze_review(review_text, preferences):
    prompt = f"""
You are analyzing a Yelp restaurant review.

Customer preferences:
{preferences}

Restaurant review:
{review_text}

Determine whether the review supports the customer's preferences.

Classify the evidence as one of:
- positive: The review supports the preferences.
- negative: The review contradicts the preferences.
- mixed: The review contains both supporting and contradicting evidence.
- insufficient: The review does not provide enough relevant information.

Use only information explicitly stated in the review.
Do not invent restaurant characteristics or explanations.

Respond using exactly this format:
Classification: positive, negative, mixed, or insufficient
Explanation: One or two sentences explaining your classification.
"""

    return ask_llm(prompt)

#Analyze a Yelp review against each customer preference independently.
#Returns:
#    dict: Evidence classification for each preference.
def analyze_review_by_preference(review_text, preferences):
    prompt = f"""
You are analyzing a Yelp restaurant review.

Customer preferences:
{json.dumps(preferences)}

Restaurant review:
{review_text}

Evaluate each customer preference independently.

For each preference, classify the review evidence as:
- positive: The review supports this preference.
- negative: The review contradicts this preference.
- mixed: The review both supports and contradicts this preference.
- insufficient: The review does not provide enough evidence.

Rules:
- Use only evidence found in the review.
- Do not invent restaurant characteristics.
- Do not require all preferences to be supported.
- A review may support one preference while providing no evidence for another.
- Return only a valid JSON object.
- Use the preference names as JSON keys.
- For each preference, include "classification" and "explanation".
- Keep explanations brief.

Example response:
{{
    "quiet": {{
        "classification": "positive",
        "explanation": "The reviewer describes the restaurant as quiet."
    }},
    "romantic": {{
        "classification": "insufficient",
        "explanation": "The reviewer does not explicitly describe a romantic setting."
    }}
}}
"""

    response = ask_llm(prompt)

    return json.loads(response)

