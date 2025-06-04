import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Page Config ---
st.title("📈 Party Cohesion Monitor")
st.markdown("Analyze how united parties are over time — and how yours compares.")

# --- Date Picker ---
st.markdown("### Select a Date Range")
date_range = st.date_input("Choose range:", [], key="date_range", help="Filter party cohesion by date range")

# --- Party Selection ---
st.markdown("### Select Parties to Compare")
parties = ["My Party", "X Party", "Y Party"]
selected_parties = st.multiselect("Parties included:", parties, default=["My Party"])

# --- Mock Cohesion Over Time Data ---
dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
data = {
    "My Party": np.random.uniform(80, 95, size=12),
    "X Party": np.random.uniform(65, 85, size=12),
    "Y Party": np.random.uniform(70, 90, size=12)
}

# --- Line Chart ---
st.markdown("### 🧭 Party Loyalty Over Time")
fig, ax = plt.subplots()
for party in selected_parties:
    ax.plot(dates, data[party], label=party)
ax.set_ylabel("% Votes in Alignment")
ax.set_xlabel("Date")
ax.set_title("Voting Cohesion Trends")
ax.legend()
st.pyplot(fig)

# --- Bar Chart (Summary for Selected Range) ---
st.markdown("### 📊 Cohesion Summary (Selected Parties)")
summary_data = pd.DataFrame({
    "Party": selected_parties,
    "% Alignment": [round(data[p].mean(), 1) for p in selected_parties],
    "% Dissent": [round(100 - data[p].mean(), 1) for p in selected_parties]
})

# Create a grouped bar chart for alignment vs. dissent
fig2, ax2 = plt.subplots()
x = np.arange(len(selected_parties))
width = 0.35
ax2.bar(x - width/2, summary_data["% Alignment"], width, label="Alignment")
ax2.bar(x + width/2, summary_data["% Dissent"], width, label="Dissent")
ax2.set_xticks(x)
ax2.set_xticklabels(selected_parties)
ax2.set_ylabel("% of Votes")
ax2.set_title("Party Cohesion Overview")
ax2.legend()
st.pyplot(fig2)

# --- Footer ---
st.markdown("---")
st.caption("Monitor trends in party loyalty and compare cohesion across EU parties.")