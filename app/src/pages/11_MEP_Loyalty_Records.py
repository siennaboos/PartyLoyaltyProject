import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from modules.nav import SideBarLinks

# Sidebar nav
SideBarLinks()

# Title
st.title("📄 MEP Party Loyalty Records")
st.markdown("Select an MEP to see their loyalty breakdown and photo.")

# Load MEPs from API
resp = requests.get("http://web-api:4000/m/meps")
meps = resp.json() if resp.status_code == 200 else []

# Build dataframe from MEPs
mep_df = pd.DataFrame()
for mep in meps:
    party_resp = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party')
    party = party_resp.json().get("partyName", "Unknown")
    mep_df = pd.concat([
        mep_df,
        pd.DataFrame([{
            "mepID": mep["mepID"],
            "name": mep["name"],
            "Party": party,
            "Country": mep["countryOfOrigin"],
            "Overall Loyalty Score": mep["loyaltyScore"]
        }])
    ], ignore_index=True)

# Dropdown
selected_mep = st.selectbox("Select MEP", mep_df["name"])
mep_row = mep_df[mep_df["name"] == selected_mep].iloc[0]
mep_id = mep_row["mepID"]

# Load dissent rate from API
response = requests.get(f"http://web-api:4000/b/get-dissent-rate?id={mep_id}")
dissent_data = response.json() if response.status_code == 200 else {}

# Create photo URL using mepID (official EP pattern)
photo_url = f"https://www.europarl.europa.eu/mepphoto/{mep_id}.jpg"

# Two-column layout (photo/info left, chart right)
col1, col2 = st.columns([1, 2])

with col1:
    st.image(photo_url, caption=selected_mep, width=160)
    st.subheader(selected_mep)
    st.markdown(f"**Party**: {mep_row['Party']}")
    st.markdown(f"**Country**: {mep_row['Country']}")
    st.markdown(f"**Overall Loyalty Score**: {mep_row['Overall Loyalty Score']}%")

with col2:
    st.markdown("### Voting Record Breakdown")

    if dissent_data:
        dissent_rate = round(dissent_data['dissent_rate'], 2)
        alignment_rate = round(100 - dissent_rate, 2)

        # Improved dual bar chart with Plotly
        fig = go.Figure(data=[
            go.Bar(name='Alignment', x=['Voting Behavior'], y=[alignment_rate], marker_color='green', width=0.4),
            go.Bar(name='Dissent', x=['Voting Behavior'], y=[dissent_rate], marker_color='crimson', width=0.4)
        ])
        fig.update_layout(
            barmode='stack',
            yaxis=dict(title="Percentage (%)", range=[0, 100]),
            title=dict(text="Alignment vs. Dissent Rate", font=dict(size=20)),
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=50, b=50),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Could not retrieve dissent rate.")