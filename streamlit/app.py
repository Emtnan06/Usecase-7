import streamlit as st
import pandas as pd
import requests


st.markdown("""
    <style>
        header {
            background-color: #ffffff;
            color: black;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-bottom: 2px solid #4a90e2;
            animation: slideIn 0.5s ease-in-out;
        }
        .title-container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logo { width: 120px; height: auto; margin-right: 15px; animation: fadeIn 1s ease-in-out; }
        .title { font-size: 42px; font-weight: bold; color: #2c3e50; text-align: center; font-family: 'Georgia', serif; }
        .sidebar .sidebar-content { background-color: #f1f1f1; border-radius: 10px; padding: 20px; }
        .sidebar .sidebar-content .stButton { background-color: #4a90e2; color: white; border-radius: 5px; padding: 10px; width: 100%; }
        .sidebar .sidebar-content .stButton:hover { background-color: #357ab7; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideIn { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .stButton { font-size: 18px; }
        .card { background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); padding: 15px; margin-bottom: 20px; }
        .card-title { font-size: 18px; font-weight: bold; color: #2c3e50; }
        .card-details { font-size: 14px; color: #7f8c8d; }
        .animated-title { font-size: 50px; color: #4188DA; animation: slideIn 1s ease-out; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Select the page")
page = st.sidebar.radio("Go to", ["Football Clustering"], label_visibility="collapsed")

# ----------------------
# ⚽ Football Clustering
# ----------------------
if page == "Football Clustering":
    with st.container():
        st.markdown("<div class='title-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image("photos/football.gif")  # Make image bigger
        with col2:
            st.markdown("<h2 class='animated-title'>Football Player Clustering</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Input fields for football features
    minutes_played = st.number_input("Minutes Played:", min_value=0, step=1)
    highest_value = st.number_input("Highest Value:", min_value=0, step=1)
    goals = st.number_input("Goals:", min_value=0, step=1)

    if st.button("Predict Football Cluster"):
        # Prepare the payload for the API
        payload = {
            "minutes_played": minutes_played,
            "highest_value": highest_value,
            "goals": goals
        }

        # API endpoint
        api_url = "https://your-football-api-endpoint.com/predict"

        # Send request to the API
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"**Cluster:** {result['cluster']}\n**Cluster Name:** {result['cluster_name']}")
            else:
                st.warning(f"⚠️ Failed to get a response. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Could not connect to the API. Error: {e}")
