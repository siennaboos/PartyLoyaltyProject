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

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import importlib.util
import os

# === Load recommender_cosine.py dynamically ===
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml-src/recommender_cosine.py"))

spec = importlib.util.spec_from_file_location("recommender_cosine", file_path)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

# === Create Flask app ===
app = Flask(__name__)

# === Load model data ===
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml-src/members_cleaned.csv"))
df = rc.make_full_df(csv_path)
df_metrics = rc.get_metrics(df)
df_encoded = rc.get_encoded_df(df_metrics)

# === Define route ===
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    filters = rc.get_filters(
        float(data["percent_agree_current"]),
        float(data["percent_attendance"]),
        data["my_party"],
        float(data["my_party_percentage"]),
        data["new_candidate_party"],
        data["new_candidate_country"]
    )

    recs = rc.get_recommendations(df, df_encoded, filters, data["my_party"])
    return jsonify(recs.to_dict(orient="records"))

# === Start app ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)