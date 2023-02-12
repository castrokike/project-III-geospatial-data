# This script contains libraries and functions that will be used to process data obtained by MongoDB queries.
# It will be called by the analysis jupyter notebook.

import pandas as pd

def get_offices_location (data):
    """
    This function will take a list (with query information from MongoDB) and return a data frame.
    It was defined because the MongoDB had nested fields that needed to be flattened.
    """
    nested_data = []
    for item in data:
        name = item['name']
        for office in item['offices']:
            nested_data.append({
                'name': name,
                'office description': office['description'],
                'office latitude': office['latitude'],
                'office longitude': office['longitude']
            })
    df = pd.DataFrame(nested_data)
    df = df.dropna(subset=["office latitude", "office longitude"], how='all')
    print("Received data for ", len(nested_data), " companies. \n", df.shape[0], " companies with full location information left.")
    return df