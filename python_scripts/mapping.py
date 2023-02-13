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

def mean_coordinates (df):
    return [round(df["office latitude"].mean(),4), round(df["office longitude"].mean(),4)]

def add_marker (name, color, icon_, coordinates, map):
    icon1 = Icon(
    color = color,
    opacity = 0.1,
    prefix = "fa", #font-awesome
    icon = icon_,
    icon_color = "white"
    )   
    marker_ = Marker(
    location = coordinates,
    tooltip = name,
    icon = icon1
    )
    marker_.add_to(map)
    return map

def sf_map(sf_center, sf_south):
    """
    This function takes that dataframes for companies in the San Francisco City Center and southern cities and plots them in a map.
    It sorts companies in their distinct groups based on the company type and city where it is located.
    """
    # Initialize the map
    sf_map = Map(location = [37.6, -122.15], zoom_start = 10)

    # Create the groups and names them according to the ammount of companies
    sf_center_tech = folium.FeatureGroup(name=f"Center Tech ({sf_center[sf_center['type'] == 'tech'].shape[0]})")
    sf_center_design = folium.FeatureGroup(name = f"Center Design ({sf_center[sf_center['type'] == 'design'].shape[0]})")
    sf_south_tech = folium.FeatureGroup(name=f"South Tech ({sf_south[sf_south['type'] == 'tech'].shape[0]})")
    sf_south_design = folium.FeatureGroup(name = f"South Design ({sf_south[sf_south['type'] == 'design'].shape[0]})")
    
    # Populates the SF Center map
    for index, row in sf_center.iterrows():
            
            # 1. Marker: creates the marker in the office location and adds the name to it.
            city = {
                "location": [row["office latitude"], row["office longitude"]],
                "tooltip": row["name"]
            }
                
            # 2. Add the icon: based on the type of company
            
            if row["type"] == "tech":
                icon = Icon (
                    color = "blue",
                    opacity = 0.5,
                    prefix="fa",
                    icon="briefcase",
                )
            else:
                icon = Icon(
                    color = "green",
                    opacity = 0.5,
                    prefix="fa",
                    icon="shirt"
                )
                
            
            # 3. Creates the map Marker
            new_marker = Marker (**city, icon = icon)
            
            # 4. Adds the marker to the corresponding group
            if row["type"] == "tech":
                new_marker.add_to(sf_center_tech)
            else:
                new_marker.add_to(sf_center_design)

    # Populates the SF South map
    for index, row in sf_south.iterrows():
            
            # 1. Marker: creates the marker in the office location and adds the name to it.
            city = {
                "location": [row["office latitude"], row["office longitude"]],
                "tooltip": row["name"]
            }
                
            # 2. Add the icon: based on the type of company
            
            if row["type"] == "tech":
                icon = Icon (
                    color = "blue",
                    opacity = 0.5,
                    prefix="fa",
                    icon="briefcase",
                )
            else:
                icon = Icon(
                    color = "green",
                    opacity = 0.5,
                    prefix="fa",
                    icon="shirt"
                )
                
            
            # 3. Creates the map Marker
            new_marker = Marker (**city, icon = icon)
            
            # 4. Adds the marker to the corresponding group
            if row["type"] == "tech":
                new_marker.add_to(sf_south_tech)
            else:
                new_marker.add_to(sf_south_design)

    # Now we add the groups to the maps
    sf_center_tech.add_to(sf_map)
    sf_center_design.add_to(sf_map)
    sf_south_tech.add_to(sf_map)
    sf_south_design.add_to(sf_map)
    
    # Find the mean coordinates for each group and city:
    sf_center_tech_mean = mean_coordinates(sf_center[(sf_center["type"] == 'tech')])
    sf_center_design_mean = mean_coordinates(sf_center[(sf_center["type"] == 'design')])
    sf_south_tech_mean = mean_coordinates(sf_south[(sf_south["type"] == 'tech')])
    sf_south_design_mean = mean_coordinates(sf_south[(sf_south["type"] == 'design')])

    # Adds the mean coordinate points to the map
    add_marker("sf_center_tech_mean","orange","computer",sf_center_tech_mean,sf_map)
    add_marker("sf_center_design_mean","red","fa-shopping-bag",sf_center_design_mean,sf_map)
    add_marker("sf_south_tech_mean","orange","computer",sf_south_tech_mean,sf_map)
    add_marker("sf_south_design_mean","red","fa-shopping-bag",sf_south_design_mean,sf_map)

    # Add the layer control
    folium.LayerControl(collapsed=False, position="topleft").add_to(sf_map)
    return sf_map

def mean_coordinates_raw (list_):
    x = 0
    y = 0
    for i in list_:
        x +=i[0]
        y +=i[1]
    x = x/len(list_)
    y = y/len(list_)

    return [round(x,4), round(y,4)]


