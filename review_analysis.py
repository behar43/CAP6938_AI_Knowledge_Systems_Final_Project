#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

from llm_client import ask_llm
import json
import time

#Convert an alternate LLM response into the expected batch structure.
def normalize_batch_response(parsed, reviews):

    if isinstance(parsed, dict) and isinstance(parsed.get("reviews"), list):
        return parsed

    if not isinstance(parsed, dict):
        return parsed

    expected_ids = {review["review_id"] for review in reviews}

    #Only normalize if the dictionary is indexed by review IDs.
    if set(parsed) != expected_ids:
        return parsed

    normalized = []

    for review_id, results in parsed.items():

        if not isinstance(results, dict):
            return parsed

        normalized_results = {}

        for preference, value in results.items():

            if not isinstance(value, dict):
                return parsed

            normalized_results[preference] = {
                "classification": value.get(
                    "classification",
                    value.get("status")
                ),
                "explanation": value.get("explanation")
            }

        normalized.append({
            "review_id": review_id,
            "results": normalized_results
        })

    return {"reviews": normalized}


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

#Analyze multiple reviews in a single LLM request.
#Returns:
#    list: Individual review analyses compatible with evidence aggregation.
def analyze_reviews_batch_once(reviews, preferences):

    if not reviews:
        return []

    import json
    from llm_client import ask_llm

    review_data = [
        {
            "review_id": review["review_id"],
            "text": review["text"]
        }
        for review in reviews
    ]

    prompt = f"""
Analyze the following Yelp restaurant reviews.

Customer preferences:
{json.dumps(preferences)}

Reviews:
{json.dumps(review_data, ensure_ascii=False)}

For EACH review, classify EACH customer preference as:
- positive: The review supports the preference.
- negative: The review contradicts the preference.
- mixed: The review contains both positive and negative evidence.
- insufficient: The review does not provide enough evidence.

Important rules:
1. Judge each review independently.
2. Classify a preference as positive or negative only when the review
   contains evidence directly relevant to that preference.
3. Do not infer positive service from the absence of service complaints.
4. Do not infer quietness from a high rating, small restaurant, or
   positive dining experience.
5. Do not infer romantic atmosphere solely from good food or service.
6. Use "insufficient" whenever the review does not provide clear evidence.
7. A review may provide evidence for multiple preferences.
8. Return valid JSON only, without Markdown or explanations outside JSON.

Return this exact JSON structure:

{{
    "reviews": [
        {{
            "review_id": "original review ID",
            "results": {{
                "preference name": {{
                    "classification": "positive",
                    "explanation": "Brief explanation based on the review"
                }}
            }}
        }}
    ]
}}

Include every supplied review and every supplied preference.
"""

#    response = ask_llm(prompt)
#    parsed = json.loads(response)

    response = ask_llm(prompt, json_mode=True)
    #Preserve the response for debugging if validation fails.
    with open("last_batch_response.json", "w", encoding="utf-8") as file:
        file.write(response)

    parsed = json.loads(response)
    parsed = normalize_batch_response(parsed, reviews)

    if not isinstance(parsed, dict) or not isinstance(parsed.get("reviews"), list):
        raise ValueError("Invalid batch response structure.")

    expected_ids = {review["review_id"] for review in reviews}
    returned_ids = [item["review_id"] for item in parsed["reviews"]]

    if len(returned_ids) != len(expected_ids) or set(returned_ids) != expected_ids:
        raise ValueError("Batch response contains missing or duplicate review IDs.")

    valid_classes = {"positive", "negative", "mixed", "insufficient"}
    original_reviews = {review["review_id"]: review for review in reviews}

    analyses_by_id = {}

    for item in parsed["reviews"]:
        review_id = item["review_id"]
        results = item["results"]

#        if not isinstance(results, dict) or set(results) != set(preferences):
#            raise ValueError(f"Invalid preferences returned for {review_id}.")

        if not isinstance(results, dict):
            raise ValueError(
                f"Invalid results structure for review {review_id}: {results}"
            )
        
        expected = set(preferences)
        actual = set(results)
        
        if actual != expected:
            raise ValueError(
                f"Preference mismatch for review {review_id}.\n"
                f"Expected: {sorted(expected)}\n"
                f"Returned: {sorted(actual)}\n"
                f"Missing: {sorted(expected - actual)}\n"
                f"Unexpected: {sorted(actual - expected)}"
            )

        for preference in preferences:
            result = results[preference]

            if (
                not isinstance(result, dict)
                or result.get("classification") not in valid_classes
                or not isinstance(result.get("explanation"), str)
            ):
                raise ValueError(
                    f"Invalid classification for {review_id}, {preference}."
                )

        original = original_reviews[review_id]

        analyses_by_id[review_id] = {
            "review_id": review_id,
            "stars": original["stars"],
            "date": original["date"],
            "results": results
        }

    return [
        analyses_by_id[review["review_id"]]
        for review in reviews
    ]

#Retry batch analysis once if the LLM returns invalid output.
def analyze_reviews_batch(reviews, preferences, max_attempts=2):

    if not reviews:
        return []

    for attempt in range(max_attempts):

        try:
            return analyze_reviews_batch_once(
                reviews,
                preferences
            )

        except (ValueError, KeyError, TypeError) as error:

            if attempt == max_attempts - 1:
                raise

            print(
                f"Batch analysis failed: {error}. "
                "Retrying..."
            )

            time.sleep(1)


