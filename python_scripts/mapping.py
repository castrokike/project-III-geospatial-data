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

def top_3_map (final_cities):
    """
    This function takes a single DataFrame with data about office locations and maps them separated into Design and Tech groups.
    It is designed to work with our specific DataFrame format.
    """
    top_3_cities_map = Map(location = [40, -99], zoom_start = 4)
    tech_group = folium.FeatureGroup(name=f"Tech ({final_cities[final_cities['type'] == 'tech'].shape[0]})")
    design_group = folium.FeatureGroup(name = f"Design ({final_cities[final_cities['type'] == 'design'].shape[0]})")

    # Iteration through DataFrame to create marker and add it to the corresponding group.
    for index, row in final_cities.iterrows():
        
        # 1. Marker: creates the marker in the office location and adds the name to it.
        city = {
            "location": [row["office latitude"], row["office longitude"]],
            "tooltip": row["name"]
        }
            
        # 2. Add the icon: based on the type of company
        
        if row["type"] == "tech":
            icon = Icon (
                color = "blue",
                prefix="fa",
                icon="briefcase",
            )
        else:
            icon = Icon(
                color = "green",
                prefix="fa",
                icon="shirt"
            )
            
        
        # 3. Creates the map Marker
        new_marker = Marker (**city, icon = icon)
        
        # 4. Adds the marker to the corresponding group
        if row["type"] == "tech":
            new_marker.add_to(tech_group)
        else:
            new_marker.add_to(design_group)
    
    # Now we add the groups to the maps
    tech_group.add_to(top_3_cities_map)
    design_group.add_to(top_3_cities_map)
    # Add the llayer control
    folium.LayerControl(collapsed=False, position="topleft").add_to(top_3_cities_map)
    return top_3_cities_map