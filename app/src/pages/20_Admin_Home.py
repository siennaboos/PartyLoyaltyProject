import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide')

SideBarLinks()

import numpy as np

st.title("🗺️ Where Should I Live Next?")
st.markdown("Explore countries by political loyalty, voter turnout, and party alignment.")

# --- MOCK DATA ---
countries = ["Germany", "France", "Spain", "Poland", "Netherlands"]

loyalty_scores = [82, 74, 88, 69, 91]
voter_turnout = [76, 72, 66, 60, 80]
science_alignment = [0.75, 0.68, 0.82, 0.57, 0.90]

# --- LOYALTY BAR CHART ---
st.markdown("### 🧭 MEP Party Loyalty by Country")
fig1, ax1 = plt.subplots()
ax1.bar(countries, loyalty_scores, color="#4CAF50")
ax1.set_ylabel("Average Loyalty Score (%)")
st.pyplot(fig1)

# --- VOTER TURNOUT ---
st.markdown("### 🗳️ Voter Turnout per Country")
fig2, ax2 = plt.subplots()
ax2.bar(countries, voter_turnout, color="#2196F3")
ax2.set_ylabel("Turnout (%)")
st.pyplot(fig2)

# --- TOPIC ALIGNMENT (e.g., Science) ---
st.markdown("### 🧪 MEP Support for Science & Environment")
fig3, ax3 = plt.subplots()
ax3.plot(countries, science_alignment, marker='o', color="#9C27B0")
ax3.set_ylabel("Alignment Score")
ax3.set_ylim(0, 1)
st.pyplot(fig3)

# --- Personalization Prompt ---
st.markdown("### 🧠 What Do You Care About?")
topic = st.radio("Choose a political issue to compare countries by:", ["Science", "Environment", "Education"])
st.markdown(f"_(Coming soon: show alignment across countries for **{topic}**)_")

# --- Footer ---
st.markdown("---")
st.caption("This page helps citizens like Greg explore where they'd feel politically aligned in the EU.")