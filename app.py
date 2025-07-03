import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime

# Load model and feature columns
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

st.set_page_config(page_title="🏠 House Price Predictor", layout="wide")
st.markdown("# 🏠 India House Price Predictor")
st.markdown("This app estimates house prices based on various property features.")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
show_gauge = st.sidebar.checkbox("Show Gauge Chart", value=True)
show_category = st.sidebar.checkbox("Show Price Category", value=True)
name = st.sidebar.text_input("🧑 Enter your name:", "User")

# Latitude and Longitude - simulate based on postal code
@st.cache_data
def get_lat_lon(postal_code):
    # Dummy simulation logic
    lat = np.random.uniform(12.0, 35.0)
    lon = np.random.uniform(70.0, 90.0)
    return lat, lon

# Inputs
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
    bathrooms = st.slider("Number of Bathrooms", 1.0, 10.0, 2.0)
    living_area = st.slider("Living Area (sqft)", 300, 10000, 2000)
    lot_area = st.slider("Lot Area (sqft)", 500, 15000, 5000)
    floors = st.slider("Number of Floors", 1.0, 4.0, 2.0)
    waterfront = st.selectbox("Waterfront Present", ["No", "Yes"])
    views = st.slider("Number of Views", 0, 4, 1)
    condition = st.slider("Condition of the House", 1, 5, 3)
    grade = st.slider("Grade of the House", 1, 13, 7)

with col2:
    area_excl_basement = st.slider("Area (Excl. Basement)", 300, 10000, 3000)
    basement_area = st.slider("Area of the Basement", 0, 5000, 0)
    built_year = st.slider("Built Year", 1900, datetime.now().year, 2000)
    renov_year = st.slider("Renovation Year", 0, datetime.now().year, 0)
    postal_code = st.number_input("Postal Code", value=100000)
    lat, lon = get_lat_lon(postal_code)
    living_area_renov = st.slider("Living Area Renovated", 0, 5000, 0)
    lot_area_renov = st.slider("Lot Area Renovated", 0, 15000, 0)
    schools_nearby = st.slider("Number of Schools Nearby", 0, 10, 3)
    airport_distance = st.slider("Distance from Airport (km)", 1, 100, 10)
    inv_distance = 1 / (airport_distance + 1)

# Encode inputs
input_dict = {
    "number_of_bedrooms": bedrooms,
    "number_of_bathrooms": bathrooms,
    "living_area": living_area,
    "lot_area": lot_area,
    "number_of_floors": floors,
    "waterfront_present": 1 if waterfront == "Yes" else 0,
    "number_of_views": views,
    "condition_of_the_house": condition,
    "grade_of_the_house": grade,
    "area_of_the_house(excluding_basement)": area_excl_basement,
    "area_of_the_basement": basement_area,
    "built_year": built_year,
    "renovation_year": renov_year,
    "postal_code": postal_code,
    "lattitude": lat,
    "longitude": lon,
    "living_area_renov": living_area_renov,
    "lot_area_renov": lot_area_renov,
    "inv_distance": inv_distance,
    "number_of_schools_nearby": schools_nearby
}

input_data = pd.DataFrame([input_dict])[columns]

# Prediction
if st.button("🔍 Predict Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Estimated House Price: ₹ {prediction:,.2f}")

    # Price Category
    if show_category:
        category = "Budget" if prediction < 30_00_000 else "Standard" if prediction < 75_00_000 else "Premium"
        st.info(f"🏷️ Category: {category}")

    # Gauge Chart
    if show_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            title={'text': "House Price (INR)"},
            gauge={'axis': {'range': [None, 2_00_00_000]},
                   'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"Developed by **Rishi Karmakar 2025**")
