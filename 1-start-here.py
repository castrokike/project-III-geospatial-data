### This script is meant to be run to initizalize the project.
### It includes query functions and other project related elements.


# Lets import all the libraries we will need:
from pymongo import MongoClient
import pandas as pd
import time
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd


# Functions we will need:

def connect_mongo(database, collection):
    client = MongoClient("localhost:27017")
    db = client[database]
    c = db.get_collection(collection)
    return c

