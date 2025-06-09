import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import streamlit as st
import pandas as pd
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

from modules.nav import SideBarLinks
SideBarLinks()

# ----------------------------
# Page Setup
# ----------------------------

st.title("📄 MEP Party Loyalty Records")
st.markdown("Search and select a Member of European Parliament (MEP) to view their party alignment, origin, loyalty score, and voting breakdown.")

# ----------------------------
# Load MEP Data via API
# ----------------------------
resp = requests.get("http://web-api:4000/m/meps")

meps = None
if resp.status_code == 200:
    meps = resp.json()
else:
    st.error("Failed to fetch MEP data.")
    st.stop()

# ----------------------------
# Build MEP DataFrame
# ----------------------------
mep_df = pd.DataFrame()

for mep in meps:
    # Get party name using mepID
    party_resp = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party')
    if party_resp.status_code == 200:
        party = party_resp.json().get("partyName", "Unknown")
    else:
        party = "Unknown"

    # Append row to DataFrame
    row = pd.DataFrame([{
        "mepID": mep["mepID"],
        "name": mep["name"],
        "Party": party,
        "Country": mep["countryOfOrigin"],
        "Overall Loyalty Score": mep["loyaltyScore"],
        "photoURL": mep.get("photoURL"),
        "% Agreed": 72,           # Placeholder values
        "% Dissented": 20,
        "% Did Not Vote": 8
    }])
    mep_df = pd.concat([mep_df, row], ignore_index=True)

# ----------------------------
# Select MEP from dropdown
# ----------------------------
selected_mep = st.selectbox("Select MEP", mep_df["name"])
selected_row = mep_df[mep_df["name"] == selected_mep].iloc[0]

# ----------------------------
# Display Photo and Info
# ----------------------------
col1, col2 = st.columns([1, 3])

with col1:
    if selected_row["photoURL"]:
        st.image(selected_row["photoURL"], caption=selected_mep, width=160)
    else:
        st.text("No photo available.")

with col2:
    st.subheader(selected_mep)
    st.markdown(f"**Party**: {selected_row['Party']}")
    st.markdown(f"**Country**: {selected_row['Country']}")
    st.markdown(f"**Overall Loyalty Score**: {selected_row['Overall Loyalty Score']}%")

# ----------------------------
# Plotly Bar Chart for Voting Breakdown
# ----------------------------
st.markdown("### Voting Record Breakdown")

vote_data = pd.DataFrame({
    "Category": ["Agreed", "Dissented", "Did Not Vote"],
    "Percentage": [
        selected_row["% Agreed"],
        selected_row["% Dissented"],
        selected_row["% Did Not Vote"]
    ]
})

fig = px.bar(
    vote_data,
    x="Category",
    y="Percentage",
    color="Category",
    color_discrete_sequence=["#4CAF50", "#9449ba", "#9E9E9E"],
    labels={"Percentage": "% of Votes"},
)
fig.update_layout(yaxis_range=[0, 100], showlegend=False)
st.plotly_chart(fig)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Explore party loyalty and voting behavior of MEPs across the European Parliament.")