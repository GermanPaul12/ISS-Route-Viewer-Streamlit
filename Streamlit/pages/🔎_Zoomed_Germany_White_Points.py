import streamlit as st
import pandas as pd
import pydeck as pdk


st.title("Germany Map 🇩🇪 with White Points ⚪️ of the ISS 📍")

# Read the CSV file into a DataFrame
data = pd.read_csv("https://raw.githubusercontent.com/GermanPaul12/ISS-Over-Mannheim-Newsletter/main/Files/iss_data.csv", names=["lat","lon","time"])

# Option to choose how many rows to show on the map from the bottom
num_rows_to_show = st.slider("Show last days", min_value=1, max_value=len(data), value=10)

# Select the last n rows from the DataFrame
data_to_show = data.iloc[-num_rows_to_show:]

# Display the first few rows of the data
st.dataframe(data_to_show.head())

# Create a new column 'tooltip' containing the date in string format
data_to_show['tooltip'] = data_to_show['time'].astype(str)

# Create a Deck.gl Scatterplot Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data_to_show,
    get_position=["lon", "lat"],
    get_radius=20000,
    get_fill_color=[255, 255, 255],  # Black color for the markers
    get_text="time",
    pickable=True,
    auto_highlight=True,
    tooltip=["time"],  # Display date on hover
)

# Set the initial view for the map
view_state = pdk.ViewState(
    latitude=51.1657,
    longitude=10.4515,
    zoom=6,
    pitch=0,
)

# Render the map
map_ = pdk.Deck(layers=[layer], initial_view_state=view_state)


# Display the map using st.pydeck_chart
st.pydeck_chart(map_)

