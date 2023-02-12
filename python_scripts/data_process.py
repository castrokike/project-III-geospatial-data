# This script contains libraries and functions that will be used to process data obtained by MongoDB queries.
# It will be called by the analysis jupyter notebook.

import pandas as pd
import geopandas as gpd

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

def load_cities(city_names):
    cities = {}
    for city_name in city_names:
        city_geo = gpd.read_file(f"data/geojsons/{city_name}.geojson")
        cities[city_name.title()] = city_geo.geometry[0]
    return cities

def add_city_name(df, cities):
    city_names = []
    for _, row in df.iterrows():
        lat, lon = row['office latitude'], row['office longitude']
        point = gpd.points_from_xy([lon], [lat])
        for city_name, city_geometry in cities.items():
            if point.within(city_geometry)[0]:
                city_names.append(city_name)
                break
        else:
            city_names.append(None)
    df['city'] = city_names
    return df