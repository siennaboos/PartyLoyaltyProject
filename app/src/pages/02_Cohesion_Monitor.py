import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks


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

SideBarLinks()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# --- Sidebar Navigation ---

# --- Page Setup ---
st.title("📊 Party Cohesion Dashboard")
st.markdown("Track dissent and alignment across EU parties with visual insights.")

# --- Date Range and Party Selection ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 📅 Date Range")
    st.date_input("Choose a time window:", [], key="date_range")

with col2:
    st.markdown("#### 🏛️ Select Parties")
    parties = ["My Party", "X Party", "Y Party"]
    selected_parties = st.multiselect("Included Parties", parties, default=parties)

# --- Mock Data ---
dates = pd.date_range(start="2023-01-01", periods=12, freq="M")
data = {
    "My Party": np.random.uniform(80, 95, size=12),
    "X Party": np.random.uniform(65, 85, size=12),
    "Y Party": np.random.uniform(70, 90, size=12)
}

# --- Dashboard Charts ---
chart_col1, chart_col2 = st.columns(2)

# --- Line Chart: Cohesion Over Time ---
with chart_col1:
    st.markdown("#### 📈 Alignment Over Time")
    fig_line = go.Figure()
    for party in selected_parties:
        fig_line.add_trace(go.Scatter(
            x=dates,
            y=data[party],
            mode='lines+markers',
            name=party,
            hovertemplate='%{y:.1f}% alignment<br>%{x|%b %Y}'
        ))
    fig_line.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=20),
        yaxis_title="% Votes Aligned",
        xaxis_title="Date",
        legend_title="Party",
        template="plotly_white"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- Bar Chart: Alignment vs. Dissent ---
with chart_col2:
    st.markdown("#### 📊 Alignment vs Dissent")
    alignment = [round(data[p].mean(), 1) for p in selected_parties]
    dissent = [round(100 - val, 1) for val in alignment]

    fig_bar = go.Figure(data=[
        go.Bar(name='Alignment', x=selected_parties, y=alignment, marker_color='green'),
        go.Bar(name='Dissent', x=selected_parties, y=dissent, marker_color='crimson')
    ])
    fig_bar.update_layout(
        barmode='group',
        height=350,
        margin=dict(l=10, r=10, t=30, b=20),
        yaxis_title="% of Votes",
        template="plotly_white",
        legend_title="Vote Type"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("Explore party cohesion trends across the EU Parliament — built with 💡 by your data team.")