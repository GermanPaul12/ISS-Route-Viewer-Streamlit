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


st.title("ISS Points 📍 when it was able to see it from Mannheim 👀 with Stats 📊")

# Read the CSV file into a DataFrame
data = pd.read_csv("https://raw.githubusercontent.com/GermanPaul12/ISS-Route-Viewer-Streamlit/main/Data/iss_data.csv", names=["lat","lon","time"])

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

# Counters for statistics
total_points = 0
total_visible_points = 0
total_distance = 0

# Add markers to the map
for index, row in data_to_show.iterrows():
    lat, lon, time = row['lat'], row['lon'], row['time']

    # Calculate the distance from Mannheim
    distance = calculate_distance(lat, lon, mannheim_lat, mannheim_lon)

    # Check if the time is between 21:00 and 07:00 and the distance is less than 500 km
    if is_iss_visible(time) and distance <= 500:
        # Determine the color and hover text for the marker
        color = "green"
        hover_text = "Could have seen the ISS"

        # Update counters
        total_visible_points += 1
        total_distance += distance
        total_points += 1
    else:
        color = "black"
        hover_text = "Probably not possible to see the ISS (too light or too far away)"
        total_points += 1
        # Skip the marker if it doesn't meet the criteria
        continue


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

# Calculate statistics
mean_distance = total_distance / total_visible_points if total_visible_points > 0 else 0
mean_time_visible = total_visible_points / total_points * 100 if total_points > 0 else 0

# Display statistics
st.subheader("Statistics")
st.write(f"Total Points: {total_points}")
st.write(f"Points Visible in Mannheim: {total_visible_points}")
st.write(f"Percentage of Points Visible in Mannheim: {mean_time_visible:.2f}%")
st.write(f"Mean Distance from Mannheim for Visible Points: {mean_distance:.2f} km")

st.info("Point is visible if: Time >= 21:00, Time <= 07:00 and Distance less than 500km")