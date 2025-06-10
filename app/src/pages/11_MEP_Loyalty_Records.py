import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.nav import SideBarLinks
SideBarLinks()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Georgia', serif !important;
        font-size: 16px;
        line-height: 1.6;
        color: #222;
    }

    h1, h2, h3, h4 {
        font-family: 'Georgia', serif !important;
    }

    .block-container {
        padding: 2rem 3rem;
    }
    </style>
""", unsafe_allow_html=True)


# Title and Instructions
st.title("📄 MEP Party Loyalty Records")
st.markdown("Select an MEP to see their loyalty breakdown and photo.")

# Load Photo CSV – place the CSV near this script or adjust accordingly
photo_df = pd.read_csv("mep_photo.csv")  # <-- move here if needed


# call backend api and get mep info
resp = requests.get("http://web-api:4000/m/meps")

meps = None
if resp.status_code == 200:
    meps = resp.json()


# # MEP Data – mock or real
mep_df = pd.DataFrame()
photo_url = "" 

for mep in meps:
    st.write(mep)
    photo_url = mep["photoURL"]
    party = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party').json()["partyName"]

    df2 = pd.DataFrame([{"name": mep["name"],
                          "Party": party,
                        "Country": mep["countryOfOrigin"],
                        "Overall Loyalty Score": mep["loyaltyScore"],
                        "% Agreed": 72,
                        "% Dissented": 28,
                        "% Did Not Vote": 8},])
    mep_df = pd.concat([mep_df, df2], ignore_index=True)




photo_df = pd.read_csv("mep_photo.csv")  

# Dropdown to select MEP
selected_mep = st.selectbox("Select MEP", mep_df["name"])
row = mep_df[mep_df["name"] == selected_mep].iloc[0]

# Match photo by MEP ID
# photo_url = photo_df.loc[photo_df["mepID"] == row["mepID"], "photo_url"].values[0]

# Layout for photo + stats
col1, col2 = st.columns([1, 3])

with col1:
    st.image(photo_url, caption=selected_mep, width=160)

with col2:
    st.subheader(selected_mep)
    st.markdown(f"**Party**: {row['Party']}")
    st.markdown(f"**Country**: {row['Country']}")
    st.markdown(f"**Overall Loyalty Score**: {row['Overall Loyalty Score']}%")

# Voting Record Breakdown
st.markdown("### Voting Record Breakdown")
labels = ["Agreed", "Dissented", "Did Not Vote"]
values = [row["% Agreed"], row["% Dissented"], row["% Did Not Vote"]]

fig, ax = plt.subplots()
ax.bar(labels, values, color=["#4CAF50", "#F44336", "#9E9E9E"])
ax.set_ylabel("% of Votes")
ax.set_ylim(0, 100)
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Use this dashboard to explore individual MEP party loyalty patterns.")