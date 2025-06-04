import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# --- Global Styling ---
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

# --- Sidebar ---
SideBarLinks()

# --- Page Setup ---
st.title("🧠 PartyLeader Recommender Dashboard")
st.markdown("#### The party recommender model proposes these MEPs as possible recruits:")

# --- Persona Context ---
with st.container():
    st.markdown("**Persona: Γιάννη Πούλος (Yanni Poulos)**  \n"
                "_Party leader concerned about internal cohesion. Wants actionable insights._")

# --- Input ---
selected_party = st.selectbox("🔽 Select Your Party", ["EPP", "S&D", "Renew Europe", "The Left"])
st.write(f"📊 Showing analysis for **{selected_party}**")

# --- Recruits Table ---
st.markdown("### 🔍 Top 5 Recruitment Candidates")

recruit_df = pd.DataFrame({
    "MEP Name": ["Lukas Werner", "Clara Johansson", "Mateo Rossi", "Eva Schmidt", "Anouk Dubois"],
    "Current Party": ["Greens/EFA", "Renew Europe", "ECR", "Greens/EFA", "The Left"],
    "% Dissent with Your Party": [12, 9, 15, 11, 10],
    "% Dissent with Their Party": [35, 28, 40, 30, 38],
    "Recent Votes With You": [7, 9, 5, 8, 6]
})

st.dataframe(recruit_df, use_container_width=True)

# --- MEP Detail ---
st.markdown("### 👤 Detailed MEP Analysis")

selected_mep = st.selectbox("Select a Candidate for Deep Dive", recruit_df["MEP Name"])
mep_row = recruit_df[recruit_df["MEP Name"] == selected_mep].iloc[0]

with st.container():
    st.markdown(f"#### 🧾 Analysis for **{selected_mep}**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Current Party:** {mep_row['Current Party']}")
        st.markdown(f"**% Dissent with Their Own Party:** {mep_row['% Dissent with Their Party']}%")
    with col2:
        st.markdown(f"**% Dissent with Your Party:** {mep_row['% Dissent with Your Party']}%")
        st.markdown(f"**Recent Votes With You:** {mep_row['Recent Votes With You']}")

    # --- Plotly Chart ---
    aligned = mep_row['Recent Votes With You']
    dissenting = 10 - aligned

    fig = go.Figure(data=[
        go.Bar(name='Aligned', x=["Recent Votes"], y=[aligned], marker_color='green'),
        go.Bar(name='Dissenting', x=["Recent Votes"], y=[dissenting], marker_color='crimson')
    ])
    fig.update_layout(
        barmode='stack',
        height=350,
        title="Recent Voting Behavior",
        yaxis_title="Number of Votes",
        template="plotly_white",
        margin=dict(l=10, r=10, t=30, b=20),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("🧭 Use this tool to explore MEPs who may be disloyal or aligned with your party.")