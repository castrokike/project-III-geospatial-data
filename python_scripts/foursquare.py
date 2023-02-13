### This script creates the nearby_office dataframe that collects all the location of the required nearby venues to our office location.

# Import all required libraries
from dotenv import load_dotenv
import os
import pandas as pd
import requests

# Load our environment
load_dotenv()

# Load our Foursquare API Key
fsq_tok = os.getenv("foursquare_key")

# Defines a function that we will use to process all the data received by the API.
def process_4sq_data(data):
    """
    This function received the json formatted response of the foursquare API and returns a DataFrame with the information for all venues received.
    The returned data frame has the columns: Name, distance from the queried point, lattitude and longitude of the venue, category id and name of the venue.
    """
    rows = []
    for result in data['results']:
        row = {
            'name': result['name'],
            'distance': result['distance'],
            'latitude': result['geocodes']['main']['latitude'],
            'longitude': result['geocodes']['main']['longitude'],
            'category_id': result['categories'][0]['id'],
            'category_name': result['categories'][0]['name']
        }
        rows.append(row)
    df = pd.DataFrame(rows).sort_values(by='distance', ascending=True)
    return df

## Query for airports
# International airports within 50 Km
url_airports = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=50000&categories=19040"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_airports = requests.get(url_airports, headers=headers)
airports_raw = response_airports.json()
airports = process_4sq_data(airports_raw)


## Query for Schools
# Pre-schools, primary and secondary schools within 12 Km
# top 30 sorted by distance 
url_schools = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=12000&categories=12056%2C12057&sort=DISTANCE&limit=30"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_schools = requests.get(url_schools, headers=headers)
schools_raw = response_schools.json()
schools = process_4sq_data(schools_raw)


## Query for Starbucks
# top 10 starbucks by distance, radius 2Km
url_starbucks = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=2000&chains=ab4c54c0-d68a-012e-5619-003048cad9da&sort=DISTANCE&limit=10"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_starbucks = requests.get(url_starbucks, headers=headers)
starbucks_raw = response_starbucks.json()
starbucks = process_4sq_data(starbucks_raw)


## Basketball
# Basketball clubs and courts within 10 Km of the office. Top 15 sorted by distance.
url_basketball = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=10000&categories=18006&sort=DISTANCE&limit=15"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_basket = requests.get(url_basketball, headers=headers)
bakset_raw = response_basket.json()
basket = process_4sq_data(bakset_raw)

## Query for vegan restaurants
# Vegan and vegetarian restaurants within 5KM (our CEO can drive) of the office. Top 20 sorted by distance.

url_vegan = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=5000&categories=13377&sort=DISTANCE&limit=20"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_vegan = requests.get(url_vegan, headers=headers)
vegan_raw = response_vegan.json()
vegan = process_4sq_data(vegan_raw)


## Pet Grooming
# Top 20 (by distance) pet grooming services on a 1.5Km radius from the office

url_pet = "https://api.foursquare.com/v3/places/search?ll=37.7824%2C-122.4039&radius=1500&categories=11134&sort=DISTANCE&limit=20"

headers = {
    "accept": "application/json",
    "Authorization": fsq_tok
}

response_pet = requests.get(url_pet, headers=headers)
pet_raw = response_pet.json()
pet = process_4sq_data(pet_raw)


## Lets create a single data frame with all our nearby spots of interest:
# First lets add a distinction to each set
pet["group"] = "Pet Grooming"
vegan["group"] = "Vegan Food"
basket["group"] = "Basket court"
starbucks["group"] = "Starbucks"
schools["group"] = "Schools"
airports["group"] = "Airports"

# Concatenate all DataFrames to a single DataFrame:
near_office = pd.concat([pet, vegan, basket, starbucks, schools, airports], axis=0)

# Finally, exports the complete DataFrame
near_office.to_csv('data/venues_near_office.csv')




