import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

import streamlit as st
import pandas as pd

st.title("🧑‍⚖️ MEPs & Party Profiles")
st.markdown("Learn more about MEPs and the political parties they represent.")

# --- MOCK DATA ---
mep_df = pd.DataFrame({
    "mep_id": [101, 102, 103, 104],
    "name": ["Anna Müller", "Tomás García", "Lena Novak", "Marc Dubois"],
    "country": ["Germany", "Spain", "Croatia", "France"],
    "party": ["S&D", "Renew Europe", "EPP", "The Left"],
    "policy_focus": ["Environment", "Digital Innovation", "Finance", "Human Rights"]
})

party_df = pd.DataFrame({
    "party": ["S&D", "Renew Europe", "EPP", "The Left"],
    "description": [
        "Center-left group supporting social equality, jobs, and climate action.",
        "Liberal, pro-European group focused on innovation, trade, and civil liberties.",
        "Center-right party advocating for economic stability and traditional values.",
        "Progressive leftist alliance fighting for social justice and anti-austerity."
    ]
})

# --- MEP Selection ---
selected_mep = st.selectbox("🔍 Select an MEP", mep_df["name"])
mep_info = mep_df[mep_df["name"] == selected_mep].iloc[0]

st.subheader(f"🇪🇺 {mep_info['name']}")
st.markdown(f"**Country**: {mep_info['country']}")
st.markdown(f"**Party**: {mep_info['party']}")
st.markdown(f"**Policy Focus**: {mep_info['policy_focus']}")

# --- Party Info ---
st.markdown("### 🏛️ Party Platform Overview")
party_description = party_df[party_df["party"] == mep_info["party"]]["description"].values[0]
st.markdown(f"**{mep_info['party']}** — {party_description}")

# --- Future Section Placeholder ---
st.markdown("---")
st.caption("Soon: Compare voting records, add favorites, and get candidate recommendations based on your views.")