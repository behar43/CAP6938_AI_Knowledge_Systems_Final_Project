#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

#Aggregate evidence classifications across multiple Yelp reviews.
#Returns:
#    dict: Classification counts for each customer preference.
def aggregate_evidence(review_analyses):
    classifications = ["positive", "negative", "mixed", "insufficient"]
    summary = {}

    for analysis in review_analyses:
        for preference, evidence in analysis["results"].items():

            if preference not in summary:
                summary[preference] = {
                    classification: 0
                    for classification in classifications
                }

            classification = evidence["classification"]

            if classification not in classifications:
                raise ValueError(
                    f"Invalid classification: {classification}"
                )

            summary[preference][classification] += 1

    return summary

