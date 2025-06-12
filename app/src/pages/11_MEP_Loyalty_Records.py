import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from modules.nav import SideBarLinks


@st.cache_data
def get_mep_data():
    # Load MEPs
    response = requests.get("http://web-api:4000/m/meps")
    if response.status_code != 200:
        st.error("Failed to load MEPs.")
        st.stop()

    meps = response.json()

    # Build DataFrame with party info
    rows = []
    for mep in meps:
        party_resp = requests.get(f"http://web-api:4000/m/meps/{mep['mepID']}/party")
        party_name = party_resp.json().get("partyName", "Unknown") if party_resp.status_code == 200 else "Unknown"

        rows.append({
            "mepID": mep["mepID"],
            "name": mep["name"],
            "party": party_name,
            "country": mep["countryOfOrigin"],
            "loyaltyScore": mep["loyaltyScore"],
            "photoURL": mep.get("photoURL")
        })

    return pd.DataFrame(rows)





# Setup
SideBarLinks()

# Title
st.title("📄 MEP Party Loyalty Records")
st.markdown("Select an MEP to see their loyalty breakdown and photo.")

# Load MEPs from API
resp = requests.get("http://web-api:4000/m/meps")
meps = resp.json() if resp.status_code == 200 else []

with st.spinner("Retrieving MEP information..."):
    mep_data = get_mep_data()

# MEP Selection
selected_name = st.selectbox("Select MEP", mep_data["name"])
selected = mep_data[mep_data["name"] == selected_name].iloc[0]

# Two-column layout (photo/info left, chart right)
col1, col2 = st.columns([1, 2])

with col1:
    st.image(selected['photoURL'], caption=selected, width=160)
    st.subheader(selected)
    st.markdown(f"**Party**: {selected['Party']}")
    st.markdown(f"**Country**: {selected['Country']}")
    st.markdown(f"**Overall Loyalty Score**: {selected['Overall Loyalty Score']}%")

with col2:
    st.markdown("### Voting Record Breakdown")

# Fetch Score Breakdown from API
score_resp = requests.get(f"http://web-api:4000/m/mep/{selected['mepID']}/score")
if score_resp.status_code == 200:
    score_data = score_resp.json()
    agreed = float(score_data.get("agreed", 0))
    dissented = float(score_data.get("dissented", 0))
    not_voted = float(score_data.get("notVoted", 0))

    
else:
    st.warning("Voting breakdown unavailable.")
    agreed, dissented, not_voted = 0, 0, 0
    dissent_data = None
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
