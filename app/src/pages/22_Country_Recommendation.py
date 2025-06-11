import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
SideBarLinks()

# --- PAGE HEADER ---
st.title("🗺️ Where Should I Live Next?")
st.markdown("Explore EU countries by political loyalty, voter turnout, and issue alignment.")

# --- MOCK DATA ---
countries = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark",
    "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal",
    "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"
]

iso_codes = [
    "AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
    "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"
]

loyalty_scores = [76.2, 93.5, 87.0, 83.0, 69.7, 82.1, 74.5, 84.8, 66.5, 78.9, 89.3, 92.5, 75.6,
                  80.4, 88.7, 65.7, 72.3, 70.8, 77.9, 85.4, 81.6, 67.4, 90.2, 69.9, 86.1, 91.5, 73.8]

voter_turnout = [70.6, 73.7, 51.9, 74.3, 56.8, 61.5, 79.1, 66.2, 67.4, 85.0, 78.8, 60.5, 69.2,
                 72.6, 75.1, 61.7, 59.4, 68.0, 54.3, 80.2, 60.3, 77.9, 63.2, 65.5, 70.9, 66.3, 88.1]


df = pd.DataFrame({
    "Country": countries,
    "ISO": iso_codes,
    "Loyalty": loyalty_scores,
    "Turnout": voter_turnout,
})

# --- USER SELECTION ---
st.markdown("### 🧠 What Do You Care About Most?")
topic = st.radio("Choose a political issue:", ["Turnout", "Loyalty"], index=0)

# --- SCORING MODEL ---
score_weights = {
    "Turnout": df["Turnout"] / 100,
    "Loyalty": df["Loyalty"] / 100
}
df["Composite Score"] = score_weights[topic]

# --- MAP: Where Should You Live? ---
st.markdown(f"### 🌍 Best Countries Based on {topic} Alignment")

fig_map = px.choropleth(
    df,
    locations="ISO",
    color="Composite Score",
    hover_name="Country",
    color_continuous_scale="Viridis",
    range_color=(0.5, 1.0),
    title=f"{topic} Alignment Across Countries"
)
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin=dict(l=0, r=0, t=50, b=0))
st.plotly_chart(fig_map, use_container_width=True)

# --- DASHBOARD CHARTS ---
st.markdown("### 📊 Country-Level Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🧭 Party Loyalty**")
    fig_loyalty = px.bar(df, x="Country", y="Loyalty", color="Loyalty", color_continuous_scale="Greens")
    fig_loyalty.update_layout(height=300, margin=dict(t=30))
    st.plotly_chart(fig_loyalty, use_container_width=True)

with col2:
    st.markdown("**🗳️ Voter Turnout**")
    fig_turnout = px.bar(df, x="Country", y="Turnout", color="Turnout", color_continuous_scale="Blues")
    fig_turnout.update_layout(height=300, margin=dict(t=30))
    st.plotly_chart(fig_turnout, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("🔍 This dashboard helps EU citizens explore where they might feel most politically aligned.")