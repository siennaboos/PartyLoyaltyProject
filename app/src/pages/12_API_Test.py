import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("📈 Party Cohesion Monitor")
st.markdown("Track how party loyalty changes over time.")

# Mock date data (replace with real later)
dates = pd.date_range(start="2023-01-01", periods=10, freq="M")

# Mock party cohesion data
mock_data = pd.DataFrame({
    "date": np.tile(dates, 3),
    "party": ["My Party"] * 10 + ["X Party"] * 10 + ["Y Party"] * 10,
    "dissent_rate": np.random.uniform(0.05, 0.25, 30)
})

# Date picker (mock range)
date_range = st.date_input("Select date range", [dates[0], dates[-1]])

# Party selection
parties = mock_data["party"].unique()
selected_parties = st.multiselect("Parties included:", parties, default=["My Party", "X Party", "Y Party"])

# Filter data
filtered_df = mock_data[
    (mock_data["party"].isin(selected_parties)) &
    (mock_data["date"] >= pd.to_datetime(date_range[0])) &
    (mock_data["date"] <= pd.to_datetime(date_range[1]))
]

# Line chart for dissent trends
st.markdown("### 📉 Dissent Rate Over Time")
fig1, ax1 = plt.subplots()
for party in selected_parties:
    party_data = filtered_df[filtered_df["party"] == party]
    ax1.plot(party_data["date"], party_data["dissent_rate"], label=party)

ax1.set_ylabel("Dissent Rate (%)")
ax1.set_xlabel("Date")
ax1.legend()
st.pyplot(fig1)

# Bar chart comparison for the selected range
st.markdown("### 📊 Dissent vs Alignment (Current Range)")
bar_data = filtered_df.groupby("party")["dissent_rate"].mean().reset_index()
bar_data["alignment_rate"] = 1 - bar_data["dissent_rate"]

fig2, ax2 = plt.subplots()
x = np.arange(len(bar_data["party"]))
ax2.bar(x - 0.2, bar_data["alignment_rate"], width=0.4, label="Alignment", color="green")
ax2.bar(x + 0.2, bar_data["dissent_rate"], width=0.4, label="Dissent", color="red")
ax2.set_xticks(x)
ax2.set_xticklabels(bar_data["party"])
ax2.set_ylabel("Average Rate (%)")
ax2.legend()
st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("Visualize party cohesion to track trends, dissent, and alignment across selected parties.")