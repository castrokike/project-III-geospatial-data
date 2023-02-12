# This script contains libraries and functions that will be used to build and display maps.
# It will be called by the analysis jupyter notebook.

from pymongo import MongoClient
import pandas as pd
import time
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd

def map_heatmap(tech_startup_data, design_companies_data):
    """
    This funcion draws a world map with two heatmaps on it. It is designed to show where in the world are these companies concentrated.
    """
    world_map = Map(location = [0, 0], zoom_start = 1)
    tech_group = folium.FeatureGroup(name=f"Tech ({tech_startup_data.shape[0]})")
    design_group = folium.FeatureGroup(name = f"Design ({design_companies_data.shape[0]})")
    HeatMap(data = tech_startup_data[["office latitude", "office longitude"]]).add_to(tech_group)
    HeatMap(data = design_companies_data[["office latitude", "office longitude"]]).add_to(design_group)
    tech_group.add_to(world_map)
    design_group.add_to(world_map)
    folium.LayerControl(collapsed=False, position="topleft").add_to(world_map)
    world_map
    return world_map