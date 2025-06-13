import streamlit as st
import requests
<<<<<<< HEAD

st.set_page_config(layout = 'wide')

SideBarLinks()

import pandas as pd

st.title("🧑‍⚖️ MEPs & Party Profiles")
st.markdown("Learn more about MEPs and the political parties they represent.")

# call backend api and get mep info
resp = requests.get("http://web-api:4000/m/meps")


meps = None
if resp.status_code == 200:
    meps = resp.json()


# # MEP Data – mock or real
mep_df = pd.DataFrame()
for mep in meps:
    party = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party').json()["partyName"]

    df2 = pd.DataFrame([{"name": mep["name"],
                          "party": party,
                        "country": mep["countryOfOrigin"],
                        "Overall Loyalty Score": mep["loyaltyScore"],
                        "% Agreed": 72,
                        "% Dissented": 28,
                        "% Did Not Vote": 8},])
    mep_df = pd.concat([mep_df, df2], ignore_index=True)


party_df = pd.DataFrame({
    "party": [
        "Group of the Progressive Alliance of Socialists and Democrats in the European Parliament",
        "Renew Europe Group",
        "Group of the European People's Party",
        "The Left group in the European Parliament",
        "Patriots for Europe Group",
        "European Conservatives and Reformists Group",
        "Group of the Greens/European Free Alliance",
        "Europe of Sovereign Nations Group"
    ],
    "description": [
        "Center-left group supporting social equality, jobs, and climate action.",
        "Liberal, pro-European group focused on innovation, trade, and civil liberties.",
        "Center-right party advocating for economic stability and traditional values.",
        "Progressive leftist alliance fighting for social justice and anti-austerity.",
        "Nationalist, euroskeptic coalition emphasizing European sovereignty and cultural heritage.",
        "Conservative-leaning alliance promoting economic liberalism and national sovereignty.",
        "Green and regionalist bloc championing environmental protection and minority rights.",
        "Right-wing group stressing national sovereignty and opposing deeper EU federalism."
    ]
})

# --- MEP Selection ---
selected_mep = st.selectbox("🔍 Select an MEP", mep_df["name"])
mep_info = mep_df[mep_df["name"] == selected_mep].iloc[0]

st.subheader(f"🇪🇺 {mep_info['name']}")
st.markdown(f"**Country**: {mep_info['country']}")
st.markdown(f"**Party**: {mep_info['party']}")

# --- Party Info ---
st.markdown("### 🏛️ Party Platform Overview")
party_description = party_df[party_df["party"] == mep_info["party"]]["description"].values[0]
st.markdown(f"**{mep_info['party']}** — {party_description}")

# --- Future Section Placeholder ---
st.markdown("---")
st.caption("Soon: Compare voting records, add favorites, and get candidate recommendations based on your views.")
=======
import pandas as pd
import plotly.express as px
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
            "percentDisagree": mep["percentDisagree"],
            "percentTurnout": mep["percentTurnout"],
            "photoURL": mep.get("photoURL")
        })

    return pd.DataFrame(rows)





# Setup
SideBarLinks()
st.title("📄 MEP Party Loyalty Records")

st.markdown("Search and select a Member of European Parliament (MEP) to view their party alignment, origin, loyalty score, and voting breakdown.")

with st.spinner("Retrieving MEP information..."):
    mep_data = get_mep_data()

# MEP Selection
selected_name = st.selectbox("Select MEP", mep_data["name"])
selected = mep_data[mep_data["name"] == selected_name].iloc[0]

# Display Headshot & Details

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


# Voting Breakdown Chart
st.markdown("### Voting Record Breakdown")

chart_df = pd.DataFrame({
    "Category": ["Agreed", "Dissented", "Turnout"],
    "Percentage": [selected["loyaltyScore"], selected["percentDisagree"], selected["percentTurnout"]]
})

fig = px.bar(
    chart_df,
    x="Category",
    y="Percentage",
    color="Category",
    color_discrete_sequence=["#4CAF50", "#9449ba", "#9E9E9E"],
    labels={"Percentage": "% of Votes"},
)
fig.update_layout(yaxis_range=[0, 100], showlegend=False)
st.plotly_chart(fig)

# Footer
st.markdown("---")
st.caption("Explore party loyalty and voting behavior of MEPs across the European Parliament.")
>>>>>>> origin/main
