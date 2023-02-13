# This script contains libraries and functions that will be used to establish mongo database connections and specific queries to it.
# It will be called by the analysis jupyter notebook.

from pymongo import MongoClient
import pandas as pd

def connect_mongo(database, collection):
    """
    This function establishes to the passed mongo database and collection.
    """
    client = MongoClient("localhost:27017")
    db = client[database]
    c = db.get_collection(collection)
    return c

def get_tech_startups (raised_ammount, year):
    """
    This function queries the ironhack database and the companies collection for tech startups that raised more than the passed ammount and that were funded after the year passed.
    It is designed to query this specific colleciton based on its structure.
    The output of the query is then casted as a list and this list is returned.
    """
    tech_startup = MongoClient("localhost:27017")["ironhack"].companies.aggregate([
        {
            "$unwind": "$funding_rounds"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {
                    "$first": "$name"
                },
                "raised_amount": {
                    "$sum": "$funding_rounds.raised_amount"
                },
                "offices": {
                    "$first": "$offices"
                },
                "category_code": {
                    "$first": "$category_code"
                },
                "founded_year": {
                    "$first": "$founded_year"
                }
            }
        },
        {
            "$match": {
                "raised_amount": {
                    "$gte": raised_ammount
                },
                "category_code": {
                    "$in": [
                        "analytics",
                        "biotech",
                        "cleantech",
                        "ecommerce",
                        "games_video",
                        "hardware",
                        "messaging",
                        "mobile",
                        "nanotech",
                        "network_hosting",
                        "search",
                        "semiconductor",
                        "social",
                        "software",
                        "transportation",
                        "travel",
                        "web"
                    ]
                },
                "founded_year": {
                    "$gte": year
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "raised_amount": 1,
                "offices": 1,
                "category_code": 1,
                "founded_year": 1
            }
        }
    ])
    ret = list(tech_startup)
    print("Query returned ",len(ret), " companies.")
    return ret

def get_design_companies ():
    """
    This function queries the ironhack database and the companies collection for design companies.
    It is designed to query this specific colleciton based on its structure.
    The output of the query is then casted as a list and this list is returned.
    """
    design_companies = MongoClient("localhost:27017")["ironhack"].companies.aggregate([
        {
            "$match": {
                "category_code": {
                    "$in": [
                        "advertising",
                        "design",
                        "fashion",
                        "photo_video"
                    ]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "offices": 1
            }
        }
    ])
    ret = list(design_companies)
    print("Query returned ",len(ret), " companies.")
    return ret