import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
SideBarLinks()

import streamlit as st
import requests

st.title("🗳️ Find Your MEP Match")
st.markdown("Answer a few questions to get MEP recommendations aligned with your values.")

# --- Form to collect user input ---
with st.form("recommender_form"):
    percent_agree_current = st.slider("How much do you agree with your current party?", 0.0, 1.0, 0.7)
    percent_attendance = st.slider("How important is attendance to you?", 0.0, 1.0, 0.85)
    my_party = st.selectbox("Your current party", [
        "Renew Europe",
        "Progressive Alliance of Socialists and Democrats",
        "European People’s Party",
        "Greens/European Free Alliance"
    ])
    my_party_percentage = st.slider("How much do you agree with your own party?", 0.0, 1.0, 0.75)
    candidate_party = st.selectbox("What party should your MEP match be from?", [
        "Renew Europe",
        "Progressive Alliance of Socialists and Democrats",
        "European People’s Party",
        "Greens/European Free Alliance"
    ])
    candidate_country = st.selectbox("Preferred country of the MEP?", [
        "France", "Germany", "Spain", "Italy", "Sweden"
    ])
    submitted = st.form_submit_button("🔍 Find Matches")

# --- Call the API ---
if submitted:
    with st.spinner("Finding your matches..."):
        response = requests.post("http://api:4000/r/generate", json={
    "percent_agree_current": 0.75,
    "percent_attendance": 0.85,
    "my_party": "Renew Europe",
    "my_party_percentage": 0.9,
    "candidate_party": "Progressive Alliance of Socialists and Democrats",
    "candidate_country": "France"
})

    if response.status_code == 200:
        matches = response.json().get("recommendations", [])
        if matches:
            st.success("🎯 Here are your top MEP matches:")
            for match in matches[:3]:  # top 3
                st.markdown(f"""
                    **{match['First Name']} {match['Last Name']}**  
                    - Country: {match['Country']}  
                    - Current Party: {match['Current Party']}  
                    - Party Alignment Rate: {round(match['Current Party Alignment Rate'] * 100)}%  
                    - Attendance Rate: {round(match['Attendance Rate'] * 100)}%  
                    - Match Score: {round(match['Cosine Score'] * 100)}%  
                """)
                st.markdown("---")
        else:
            st.warning("No MEPs matched your criteria. Try broadening your filters.")
    else:
        st.error(f"Error: {response.status_code} – {response.text}")