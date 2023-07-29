# Import libraries
import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go

# Read csv and manipulate data to desired format
url = 'https://raw.githubusercontent.com/GermanPaul12/ISS-Route-Viewer-Replit-and-Streamlit/main/Data/iss_data.csv'
df = pd.read_csv(url, names=["lat", "lon", "time"])
time_converter = lambda x: x[:-7]
df.time = df.time.apply(time_converter)
df.time = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")
df["day"] = df.time.dt.to_period('D')
df.lat = pd.to_numeric(df.lat)
df.lon = pd.to_numeric(df.lon)

# create title
st.title("ISS Route Viewer 📍")

# check if data is in the desired format
#print(df.time)
#print(df.dtypes)
#print(df.day)



# creat df_time 
def create_df_time(start,end):
    lo,hi = int(df[df.day == start].index[0]),int(df[df.day == end].index[0])
    return df.iloc[lo:hi+1]

# Create slider choose datetime
col1,col2 = st.columns(2)
with col1:
    starting_time = st.selectbox("Start Date:", df.day.sort_values(ascending=False).unique(), index=1)
with col2:
    end_time = st.selectbox("End Date:", df.day.sort_values(ascending=False).unique(), index=0)

if end_time < starting_time:
    st.warning("Please make the starting time smaller than the end time")    
    

data = create_df_time(starting_time, end_time)

fig = go.Figure()

r,g,b=0,0,0

for i, day in enumerate(data.day.unique()):
    #print(data[(data.day == day) == True]) 
    fig.add_trace(go.Scattergeo(                          
        lon = data[data.day == day].lon, 
        lat = data[data.day == day].lat,
        mode = 'lines',
        line = dict(width = 2, color = f'rgb({r},{g},{b})'
        )))
    r = r + random.randint(0,255) % 256
    g = g + random.randint(0,255) % 256
    b = b + random.randint(0,255) % 256

fig.update_layout(
    title_text = 'Contour lines over globe<br>(Click and drag to rotate)',
    showlegend = False,
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        
        countrywidth = 0.5,
        landcolor = 'rgb(230, 145, 56)',
        lakecolor = 'rgb(0, 255, 255)',
        oceancolor = 'rgb(0, 255, 255)',
        bgcolor = '#121212',
        projection = dict(
            type = 'orthographic',
            rotation = dict(
                lon = -100,
                lat = 40,
                roll = 0
            )
        ),
        lonaxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        ),
        lataxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        )
    )
)

st.plotly_chart(fig)
