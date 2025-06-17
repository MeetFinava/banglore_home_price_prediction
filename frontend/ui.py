import streamlit as st
import json
import requests

# Load location list from location.json
with open("../model/locationjson.json", "r") as f:
    locations = json.load(f)

st.set_page_config(page_title="🏠 Bangalore House Price Predictor", layout="centered")

st.title("🏠 Bangalore House Price Predictor")
st.markdown("Estimate the property price based on input features.")

# --- User Inputs ---
location = st.selectbox("📍 Location", sorted(locations))
total_sqft = st.number_input("📏 Total Square Feet", min_value=300, max_value=10000, step=10)
bath = st.selectbox("🛁 Number of Bathrooms", list(range(1, 6)))
bhk = st.selectbox("🛏️ Number of BHK", list(range(1, 6)))

# --- Submit Button ---
if st.button("Predict Price 💰"):
    payload = {
        "location": location,
        "total_sqft": total_sqft,
        "bathrooms": bath,
        "bhk": bhk
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            price = response.json()["estimated_price_in_lakhs"]
            st.success(f"🏡 Estimated Price: ₹ {price} Lakhs")
        else:
            st.error("⚠️ Failed to get prediction from the API.")
    except Exception as e:
        st.error(f"❌ Error: {e}")