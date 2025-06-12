import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

import plotly.graph_objects as go

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

SideBarLinks()


# --- Sidebar Navigation ---

# --- Page Setup ---
st.title("📊 Percent Dissent Predictor")
st.markdown("Want to see how unified a party will be on a certain type of vote? Choose a party and procedure type"
" to predict percent dissent.")

# --- Party and Procedure Type Selection ---
st.markdown("#### 🏛️ Select Parties")
party_dict = {
    "European Conservatives and Reformists": "ECR",
    "European People's Party": "EPP",
    "Europe of Sovereign Nations": "ESN",
    "The Left in the European Parliament – Nordic Green Left": "GUE/NGL",
    "The Greens/European Free Alliance": "Greens/EFA",
    "Identity and Democracy": "ID",
    "Patriots for Europe": "Patriots for Europe",
    "Renew Europe": "Renew",
    "Progressive Alliance of Socialists and Democrats": "S&D"
}

procedure_dict = {
    'Act for Codification Initiative': 'ACI',
    'Approval procedure': 'APP',
    'Budget procedure': 'BUD',
    'Budgetary Control procedure': 'BUI',
    'Consultation procedure': 'CNS',
    'Ordinary legislative procedure (formerly co-decision)': 'COD',
    'Delegated act': 'DEA',
    'Discharge procedure': 'DEC',
    'Own-initiative procedure': 'INI',
    'Legislative initiative procedure': 'INL',
    'Consent procedure (formerly assent)': 'NLE',
    'Rule change or internal regulation': 'REG',
    'Resolution procedure (Special)': 'RPS',
    'Rule of Procedure (Organisational)': 'RSO',
    'Non-legislative resolution': 'RSP'
}

selected_parties = st.multiselect("Included Parties", party_dict.keys(), default=None)
selected_procedures = st.multiselect("Included Procedure Types", procedure_dict.keys(), default=None)

# --- Dashboard Charts ---
chart_col1, chart_col2 = st.columns(2)

# Make Prediction
input = {
    'Parties' : selected_parties,
    'Procedures' : selected_procedures
}
headers = {
    "Content Type": "application/json"
}

response = requests.get(f"http://web-api:4000/l/prediction", headers=headers, params=input)
st.write(response.status_code)
st.write(response.json)

predicted_dissent = response.json()

# Displaying dissent prediction (mock rn)
st.markdown("#### 📈 Predicted Dissent From Party Majority")
st.metric('Percent Dissent', predicted_dissent, border=True)

# --- Bar Chart: Alignment vs. Dissent ---
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