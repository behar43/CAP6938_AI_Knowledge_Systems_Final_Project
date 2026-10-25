#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import hashlib
import json
from pathlib import Path


CACHE_VERSION = 1
CACHE_DIRECTORY = Path("analysis_cache")


#Generate a unique key for a restaurant analysis.
def make_cache_key(
    business_id,
    preferences,
    preference_queries,
    review_limit,
    retrieval_method="semantic",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    llm_model="qwen3:4b"
):

    parameters = {
        "cache_version": CACHE_VERSION,
        "business_id": business_id,
        "preferences": preferences,
        "preference_queries": preference_queries,
        "review_limit": review_limit,
        "retrieval_method": retrieval_method,
        "embedding_model": embedding_model,
        "llm_model": llm_model
    }

    serialized = json.dumps(
        parameters,
        sort_keys=True
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


#Load a completed restaurant analysis, if available.
def load_cached_analysis(cache_key):

    cache_file = CACHE_DIRECTORY / f"{cache_key}.json"

    if not cache_file.exists():
        return None

    with open(cache_file, "r", encoding="utf-8") as file:
        return json.load(file)


#Save a completed restaurant analysis.
def save_cached_analysis(cache_key, analysis):

    CACHE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    cache_file = CACHE_DIRECTORY / f"{cache_key}.json"
    temporary_file = cache_file.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(
            analysis,
            file,
            indent=2,
            ensure_ascii=False
        )

    #Replace the destination only after writing completes.
    temporary_file.replace(cache_file)

    return cache_file
