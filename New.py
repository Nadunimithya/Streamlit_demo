import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load Data
csv_file_path = r"https://github.com/Nadunimithya/Streamlit_demo/blob/main/us-population-2010-2019-states-code.csv"
data = pd.read_csv(csv_file_path)

# Load Shapefile Data
shapefile_path = r"https://github.com/Nadunimithya/Streamlit_demo/blob/main/USA_names.shp"
gdf = gpd.read_file(shapefile_path)

# Convert columns to strings for consistent handling
data.columns = [str(col) for col in data.columns]

# Set Streamlit Page Config
st.set_page_config(page_title="USA Population Trends", layout="wide")

# Sidebar Configuration
with st.sidebar:
   
    
    # Dropdown for year selection
    selected_year = st.selectbox("Select Year", options=[str(year) for year in range(2010, 2020)], index=0)
    
    # Dropdown for state selection
    selected_state = st.selectbox("Select State", options=data["states"].unique(), index=0)

# Filter Data Based on User Selection
filtered_data = data[["states", "states_code", selected_year]]
filtered_data = filtered_data[filtered_data["states"] == selected_state]


# Main Area
st.title("USA Population Trends Dashboard")

# Create two columns for layout
col1, col2 = st.columns([2, 1])  # Adjust column width ratio as needed


# Left Column: Interactive Map and Line Chart
with col1:
    # Interactive Map
    center_coords = [37.8, -96.9]  # Approximate center of the USA
    m = folium.Map(location=center_coords, zoom_start=4, tiles="cartodbpositron")

    # Add GeoJSON from the shapefile to the map
    folium.GeoJson(
        gdf,
        name="USA States",
        tooltip=folium.GeoJsonTooltip(fields=["NAME"], aliases=["STATE:"]),
        style_function=lambda x: {
            "fillColor": "#3186cc",
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.3,
        }
    ).add_to(m)

    # Display the Folium map in Streamlit
    st_folium(m, width=700, height=400)

    # Line Chart for Population Trends
    if not filtered_data.empty:
        st.write(f"Population: **{filtered_data[selected_year].values[0]}** in the year {selected_year}")
    else:
        st.warning("No data available for the selected filters.")

    melted_data = data[data["states"] == selected_state].melt(
        id_vars=["states", "states_code"],
        value_vars=[str(year) for year in range(2010, 2020)],
        var_name="Year",
        value_name="Population"
    )
    melted_data["Year"] = melted_data["Year"].astype(int)

    line_chart = px.line(
        melted_data,
        x="Year",
        y="Population",
        markers=True
    )
    st.plotly_chart(line_chart, use_container_width=True, key="line_chart_key")

# Right Column: Table of Top 10 States by Population
with col2:
    st.subheader("Top 10 States by Population")
    
    # Filter data for the selected year and sort by population
    top_10_states = data[["states", selected_year]].sort_values(
        by=selected_year, ascending=False
    ).head(10)
    
    # Display the table
    st.table(top_10_states.rename(columns={selected_year: "Population"}))
