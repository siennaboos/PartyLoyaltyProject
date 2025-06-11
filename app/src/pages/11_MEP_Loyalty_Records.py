import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

# Setup
SideBarLinks()
st.title("📄 MEP Party Loyalty Records")
st.markdown("Search and select a Member of European Parliament (MEP) to view their party alignment, origin, loyalty score, and voting breakdown.")

# ----------------------------
# Load MEPs
# ----------------------------
response = requests.get("http://web-api:4000/m/meps")
if response.status_code != 200:
    st.error("Failed to load MEPs.")
    st.stop()

meps = response.json()

# ----------------------------
# Build DataFrame with party info
# ----------------------------
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

df = pd.DataFrame(rows)

# ----------------------------
# MEP Selection
# ----------------------------
selected_name = st.selectbox("Select MEP", df["name"])
selected = df[df["name"] == selected_name].iloc[0]

# ----------------------------
# Display Headshot & Details
# ----------------------------
col1, col2 = st.columns([1, 3])
with col1:
    if selected["photoURL"]:
        st.image(selected["photoURL"], width=160, caption=selected_name)
    else:
        st.write("No photo available.")

with col2:
    st.subheader(selected_name)
    st.markdown(f"**Party**: {selected['party']}")
    st.markdown(f"**Country**: {selected['country']}")
    st.markdown(f"**Overall Loyalty Score**: {selected['loyaltyScore']}%")

# ----------------------------
# Fetch Score Breakdown from API
# ----------------------------
response = requests.get("http://web-api:4000/b/alignment-dissent")  # update route if different

if response.status_code != 200:
    st.error("Failed to load alignment data.")
    st.stop()

data = response.json()  # Expecting list of dicts like {"party": ..., "alignment": ..., "dissent": ...}

df = pd.DataFrame(data)

# Filter for selected_parties
df = df[df["party"].isin(selected_parties)]

# -----------------------------------------
# Plot bar chart
# -----------------------------------------
with chart_col2:
    st.markdown("#### 📊 Alignment vs Dissent")

    fig_bar = go.Figure(data=[
        go.Bar(name='Alignment', x=df['party'], y=df['alignment'], marker_color='green'),
        go.Bar(name='Dissent', x=df['party'], y=df['dissent'], marker_color='crimson')
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

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Explore party loyalty and voting behavior of MEPs across the European Parliament.")