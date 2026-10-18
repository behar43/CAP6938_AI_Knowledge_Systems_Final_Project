#Author: Ben Prishtina
#Class: CAP 6938: AI Knowledge

import json
from pathlib import Path

# Default location of the Yelp working dataset.
DATA_DIR = Path(__file__).resolve().parent.parent / "Yelp_JSON"

BUSINESS_FILE = DATA_DIR / "tampa_restaurants.json"

#Load restaurant records from a JSON Lines file.
#Returns:
#    dict: Restaurant records indexed by business_id.
def load_restaurants(file_path=BUSINESS_FILE):
    restaurants = {}

    with Path(file_path).open("r", encoding="utf-8") as f:
        for line in f:
            business = json.loads(line)
            restaurants[business["business_id"]] = business
    return restaurants

#Retrieve a restaurant by its business_id.
#Returns None if the restaurant is not found.
def get_restaurant(restaurants, business_id):
    return restaurants.get(business_id)

