#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

#Calculate preference scores from aggregated review evidence.
#Returns:
#    dict: Scores and evidence counts for each preference.
def score_restaurant(evidence_summary):
    scores = {}

    for preference, counts in evidence_summary.items():
        positive = counts["positive"]
        negative = counts["negative"]
        mixed = counts["mixed"]
        insufficient = counts["insufficient"]

        # Only reviews with relevant evidence contribute to the score.
        evidence_count = positive + negative + mixed

        if evidence_count == 0:
            score = None
        else:
            score = (positive - negative) / evidence_count

        # Simple indicator of how much evidence was analyzed.
        if evidence_count == 0:
            confidence = "no evidence"
        elif evidence_count < 5:
            confidence = "limited"
        elif evidence_count < 20:
            confidence = "moderate"
        else:
            confidence = "substantial"

        scores[preference] = {
            "score": score,
            "evidence_count": evidence_count,
            "insufficient_count": insufficient,
            "confidence": confidence
        }

    return scores

