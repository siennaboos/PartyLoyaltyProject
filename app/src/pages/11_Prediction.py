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

# Title and Instructions
st.title("📄 MEP Party Loyalty Records")
st.markdown("Select an MEP to see their loyalty breakdown and photo.")

# Load Photo CSV – place the CSV near this script or adjust accordingly
photo_df = pd.read_csv("mep_photo.csv")  # <-- move here if needed

# MEP Data – mock or real
mep_df = pd.DataFrame({
    "mep_id": [1, 2, 3, 4],
    "MEP Name": ["Anna Müller", "Tomás García", "Lena Novak", "Marc Dubois"],
    "Party": ["S&D", "Renew Europe", "EPP", "The Left"],
    "Country": ["Germany", "Spain", "Croatia", "France"],
    "Overall Loyalty Score": [84, 91, 76, 88],
    "% Agreed": [72, 85, 66, 80],
    "% Dissented": [20, 10, 28, 15],
    "% Did Not Vote": [8, 5, 6, 5]
})

# Dropdown to select MEP
selected_mep = st.selectbox("Select MEP", mep_df["MEP Name"])
row = mep_df[mep_df["MEP Name"] == selected_mep].iloc[0]

# Match photo by MEP ID
photo_url = photo_df.loc[photo_df["mep_id"] == row["mep_id"], "photo_url"].values[0]

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