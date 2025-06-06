import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from modules.nav import SideBarLinks
SideBarLinks()

import importlib.util
import os

"""

"""
st.title("Party Loyalty Recommender")

# Input fields
agree_current = st.slider("Current Party Agreement (%)", 0.0, 1.0, 0.7)
attendance = st.slider("Attendance Rate (%)", 0.0, 1.0, 0.6)
my_party = st.selectbox("Your Party", [
    'European People’s Party', 'Renew Europe', 'Progressive Alliance of Socialists and Democrats',
    'European Conservatives and Reformists', 'Non-attached Members', 'Europe of Sovereign Nations',
    'The Left in the European Parliament – GUE/NGL', 'Greens/European Free Alliance', 
    'Patriots for Europe', 'Identity and Democracy'
])
my_party_pct = st.slider("Your Party Loyalty (%)", 0.0, 1.0, 0.7)
candidate_party = st.selectbox("Candidate's Party", [
    'European People’s Party', 'Renew Europe', 'Progressive Alliance of Socialists and Democrats',
    'European Conservatives and Reformists', 'Non-attached Members', 'Europe of Sovereign Nations',
    'The Left in the European Parliament – GUE/NGL', 'Greens/European Free Alliance', 
    'Patriots for Europe', 'Identity and Democracy'
])
candidate_country = st.selectbox("Candidate's Country", [
    'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France',
    'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
    'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'
])

if st.button("Get Recommendations"):
    response = requests.post("http://localhost:5000/recommend", json={
        "percent_agree_current": agree_current,
        "percent_attendance": attendance,
        "my_party": my_party,
        "my_party_percentage": my_party_pct,
        "new_candidate_party": candidate_party,
        "new_candidate_country": candidate_country
    })



    if response.status_code == 200:
        recs = pd.DataFrame(response.json())

        st.write("### Top Recommended MEPs")
        st.dataframe(recs)

        st.write("### Cosine Similarity of Top 10 MEPs")
        fig, ax = plt.subplots()
        ax.barh(recs["first_name"] + " " + recs["last_name"], recs["mep_cosine"])
        ax.invert_yaxis()
        ax.set_xlabel("Cosine Similarity")
        ax.set_title("Top MEP Matches")
        st.pyplot(fig)
    else:
        st.error("Something went wrong with the backend call.")