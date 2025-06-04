import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# --- Page setup ---
st.title("🧠 Party Leader Recommender Dashboard")
st.subheader("Identify MEPs who may be disloyal or worth recruiting")

# --- Persona Context ---
st.markdown("""
**Persona: Γιάννη Πούλος (Yanni Poulos)**  
Party leader concerned about internal cohesion. Wants actionable insights.
""")

# --- Mock Inputs ---
selected_party = st.selectbox("Select Your Party", ["EPP", "S&D", "Renew Europe", "The Left"])
st.write(f"Showing analysis for **{selected_party}**")

# --- Mock Table for Recruitment Candidates ---
st.markdown("### 🔍 Potential Recruits")
st.markdown("These MEPs vote closely with your party but are not members of it.")

recruit_df = pd.DataFrame({
    "MEP Name": ["Lukas Werner", "Clara Johansson", "Mateo Rossi", "Eva Schmidt", "Anouk Dubois"],
    "Current Party": ["Greens/EFA", "Renew Europe", "ECR", "Greens/EFA", "The Left"],
    "% Dissent with Your Party": [12, 9, 15, 11, 10],
    "% Dissent with Their Party": [35, 28, 40, 30, 38],
    "Recent Votes With You": [7, 9, 5, 8, 6]
})

st.dataframe(recruit_df)

# --- MEP Click Logic ---
st.markdown("### 👥 Select a MEP to View Party Fit")
selected_mep = st.selectbox("Select a Potential MEP", recruit_df["MEP Name"])

mep_row = recruit_df[recruit_df["MEP Name"] == selected_mep].iloc[0]

with st.expander(f"📋 Analysis for {selected_mep}"):
    st.markdown(f"**Current Party**: {mep_row['Current Party']}")
    st.markdown(f"**Percent of Votes Dissenting With Your Party**: {mep_row['% Dissent with Your Party']}%")
    st.markdown(f"**Percent of Votes Dissenting With Their Party**: {mep_row['% Dissent with Their Party']}%")
    st.markdown(f"**Recent Votes in Alignment with You**: {mep_row['Recent Votes With You']}")

    # Placeholder chart for recent voting behavior
    fig, ax = plt.subplots()
    ax.bar(["Aligned", "Dissenting"], [mep_row['Recent Votes With You'], 10 - mep_row['Recent Votes With You']])
    ax.set_ylabel("# of Votes")
    st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.caption("This dashboard helps party leaders identify internal risks and external opportunities.")