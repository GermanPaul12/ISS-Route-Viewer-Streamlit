import streamlit as st
import pandas as pd
import folium
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, time as dt_time

def calculate_distance(lat1, lon1, lat2, lon2):
    # The radius of the Earth in km
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def is_iss_visible(time_str):
    # Convert time string to datetime object
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

    # Extract the time part from the datetime object
    time_part = time_obj.time()

    # Define time objects for 21:00 and 07:00
    time_21 = dt_time(21, 0)
    time_7 = dt_time(7, 0)

    # Check if the time is between 21:00 and 07:00
    return time_21 <= time_part or time_part < time_7

st.title("🇩🇪 Germany Map with 📍 Locations and ⏰ Times")

# Read the CSV file into a DataFrame
data = pd.read_csv("https://raw.githubusercontent.com/GermanPaul12/ISS-Over-Mannheim-Newsletter/main/Files/iss_data.csv", names=["lat","lon","time"])

# Display the first few rows of the data
st.dataframe(data.head())

# Option to choose how many rows to show on the map from the bottom
num_rows_to_show = st.slider("Show last days", min_value=1, max_value=len(data), value=10)

# Select the last n rows from the DataFrame
data_to_show = data.iloc[-num_rows_to_show:]

# Create a map centered around Germany
map_center = [51.1657, 10.4515]
folium_map = folium.Map(location=map_center, zoom_start=6)

# Define Mannheim coordinates
mannheim_lat, mannheim_lon = 49.4875, 8.4660

# Add markers to the map
for index, row in data_to_show.iterrows():
    lat, lon, time = row['lat'], row['lon'], row['time']

    # Calculate the distance from Mannheim
    distance = calculate_distance(lat, lon, mannheim_lat, mannheim_lon)

    # Check if the time is between 22:00 and 06:00
    is_night_time = is_iss_visible(time)

    # Determine the color and hover text for the marker
    if distance <= 500 and is_night_time:
        color = "green"
        hover_text = "Could have seen the ISS"
    else:
        color = "black"
        hover_text = "Probably not possible to see the ISS (too light or too far away)"

    # Add the marker to the map
    folium.Marker(
        location=[lat, lon],
        tooltip=f"Date: {time}<br>Lat: {lat:.5f}<br>Lon: {lon:.5f}<br>Distance from Mannheim: {distance:.2f} km",
        icon=folium.Icon(color=color),
        popup=hover_text,
    ).add_to(folium_map)

# Use IFrame to display the Folium map in Streamlit
map_html = folium_map.get_root().render()
st.components.v1.html(map_html, height=500)

st.info("Points are Green if the time is greater than 21:00 (9 PM), smaller than 07:00 (7 AM) and distance is less than 500km (310 Miles)")
