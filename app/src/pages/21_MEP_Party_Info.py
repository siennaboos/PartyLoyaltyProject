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

# call backend api and get mep info
resp = requests.get("http://web-api:4000/m/meps")


meps = None
if resp.status_code == 200:
    meps = resp.json()


# # MEP Data – mock or real
mep_df = pd.DataFrame()
for mep in meps:
    party = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party').json()["partyName"]

    df2 = pd.DataFrame([{"name": mep["name"],
                          "party": party,
                        "country": mep["countryOfOrigin"],
                        "Overall Loyalty Score": mep["loyaltyScore"],
                        "% Agreed": 72,
                        "% Dissented": 28,
                        "% Did Not Vote": 8},])
    mep_df = pd.concat([mep_df, df2], ignore_index=True)


party_df = pd.DataFrame({
    "party": [
        "Group of the Progressive Alliance of Socialists and Democrats in the European Parliament",
        "Renew Europe Group",
        "Group of the European People's Party",
        "The Left group in the European Parliament",
        "Patriots for Europe Group",
        "European Conservatives and Reformists Group",
        "Group of the Greens/European Free Alliance",
        "Europe of Sovereign Nations Group"
    ],
    "description": [
        "Center-left group supporting social equality, jobs, and climate action.",
        "Liberal, pro-European group focused on innovation, trade, and civil liberties.",
        "Center-right party advocating for economic stability and traditional values.",
        "Progressive leftist alliance fighting for social justice and anti-austerity.",
        "Nationalist, euroskeptic coalition emphasizing European sovereignty and cultural heritage.",
        "Conservative-leaning alliance promoting economic liberalism and national sovereignty.",
        "Green and regionalist bloc championing environmental protection and minority rights.",
        "Right-wing group stressing national sovereignty and opposing deeper EU federalism."
    ]
})

# --- MEP Selection ---
selected_mep = st.selectbox("🔍 Select an MEP", mep_df["name"])
mep_info = mep_df[mep_df["name"] == selected_mep].iloc[0]

st.subheader(f"🇪🇺 {mep_info['name']}")
st.markdown(f"**Country**: {mep_info['country']}")
st.markdown(f"**Party**: {mep_info['party']}")

# --- Party Info ---
st.markdown("### 🏛️ Party Platform Overview")
party_description = party_df[party_df["party"] == mep_info["party"]]["description"].values[0]
st.markdown(f"**{mep_info['party']}** — {party_description}")

# --- Future Section Placeholder ---
st.markdown("---")
st.caption("Soon: Compare voting records, add favorites, and get candidate recommendations based on your views.")