import streamlit as st
<<<<<<< HEAD
from streamlit_extras.app_logo import add_logo
import pandas as pd
from modules.nav import SideBarLinks
import plotly.graph_objects as go
import requests
import plotly.express as px

SideBarLinks()

# --- Page Setup ---
st.title("📊 Percent Dissent Predictor")
st.markdown("Want to see how unified a party will be on a certain type of vote? Choose a party and procedure type"
" to predict percent dissent.")

# --- Party and Procedure Type Selection ---
st.markdown("#### 🏛️ Select Parties and Procedure Types")
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

input = {
    'parties' : [party_dict[party] for party in selected_parties],
    'procedures' : [procedure_dict[procedure] for procedure in selected_procedures]
}

logger.info(selected_procedures)

response = requests.post(f"http://web-api:4000/l/prediction", json=input)

if response.status_code != 200:
    st.write("Could not make a prediction :(")
    st.stop()

predicted_dissent = response.json()

# Displaying dissent prediction
st.markdown("#### 📈 Predicted Dissent From Party Majority")
if st.button('Predict Dissent', use_container_width=False):
    st.metric('Percent Dissent', predicted_dissent['prediction'], border=True)

# --- Bar Chart: Alignment vs. Dissent ---
st.markdown("#### 📊 Average Loyalty Score for Each Party")
st.write('This visualization shows the average loyalty score for MEPs in every party in the EU. Loyalty scores are calculated based on dissent and alignment rates.')
st.write('\'Dissent\' refers to the action of an MEP voting differently than the majority of MEPs in their formally affiliated party.')

# ----------------------------
# Load MEP data from API
# ----------------------------
resp = requests.get("http://web-api:4000/m/meps")
meps = resp.json() if resp.status_code == 200 else []

# ----------------------------
# Build DataFrame with party info
# ----------------------------
mep_df = pd.DataFrame()
for mep in meps:
    try:
        party_resp = requests.get(f'http://web-api:4000/m/meps/{mep["mepID"]}/party')
        party = party_resp.json().get("partyName", "Unknown")
    except:
        party = "Unknown"

    row = pd.DataFrame([{
        "mepID": mep["mepID"],
        "party": party,
        "loyalty": float(mep["loyaltyScore"]),
    }])
    mep_df = pd.concat([mep_df, row], ignore_index=True)

mep_df.replace('European Peopleâ€™s Party', 'European Peoples\' Party', inplace=True)
party_df = mep_df.groupby("party", as_index=False)["loyalty"].mean()


fig = px.bar(party_df, x='party', y='loyalty', labels={'party': 'Party', 'loyalty': 'Average Loyalty Score'},
    width=600, height=800)

# Angle the x-axis labels
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=False)

# --- Footer ---
st.markdown("---")
st.caption("Explore party cohesion trends across the EU Parliament — built by the Loyalty Lines data team 💡")
=======
import requests
from modules.nav import SideBarLinks

# Sidebar nav
SideBarLinks()

# Constants
USER_ID = 1
WATCHLIST_URL = f"http://web-api:4000/w/user/{USER_ID}/watchlists"
ALL_MEPS_URL = "http://web-api:4000/w/all_meps"

# Fetch watchlist
def get_watchlist():
    try:
        res = requests.get(WATCHLIST_URL)
        if res.status_code == 200:
            return res.json()
        st.error(f"Watchlist error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"Watchlist fetch failed: {e}")
    return []

# Fetch MEPs for dropdown
def get_all_meps():
    try:
        res = requests.get(ALL_MEPS_URL)
        if res.status_code == 200:
            return res.json()
        st.error(f"MEP list error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"MEP list fetch failed: {e}")
    return []

# Add MEP
def add_to_watchlist(mep_id):
    try:
        res = requests.post(WATCHLIST_URL, json={"mepID": mep_id})
        if res.status_code == 201:
            st.success("✅ MEP added.")
            st.rerun()
        elif res.status_code == 409:
            st.warning("⚠️ MEP already in watchlist.")
        else:
            msg = res.json().get("error", "Something went wrong.")
            st.error(f"❌ Failed to add: {msg}")
    except Exception as e:
        st.error(f"Add failed: {e}")

# Remove MEP
def remove_from_watchlist(mep_id):
    try:
        res = requests.delete(WATCHLIST_URL, json={"mepID": mep_id})
        if res.status_code == 200:
            st.success("🗑️ MEP removed.")
            st.rerun()
        else:
            st.error(f"Remove failed: {res.text}")
    except Exception as e:
        st.error(f"Remove error: {e}")

# ---------- UI ----------

st.title("👀 Current Watchlist")
watchlist = get_watchlist()

if not watchlist:
    st.info("No MEPs in your watchlist yet.")
else:
    for mep in watchlist:
        with st.container():
            st.markdown("---")
            cols = st.columns([1, 3])
            with cols[0]:
                mep_id = mep.get("mepID")
                photo_url = f"https://www.europarl.europa.eu/mepphoto/{mep_id}.jpg" if mep_id else ""
                st.image(photo_url, width=100)
            with cols[1]:
                st.markdown(f"### {mep.get('name', 'Unnamed MEP')}")
                st.markdown(f"**🌍 Country**: {mep.get('countryOfOrigin', 'Unknown')}")
                st.markdown(f"**📊 Loyalty Score**: {mep.get('loyaltyScore', '?')}")
                st.markdown(f"**🏛️ Party ID**: {mep.get('partyID')} → Recommended: {mep.get('recommendedPartyID')}")
                if mep_id:
                    st.button(
                        "❌ Remove",
                        key=f"remove_{mep_id}_{mep['name']}",
                        on_click=remove_from_watchlist,
                        args=(mep_id,)
                    )

# Divider
st.markdown("## ➕ Add MEP to Watchlist")

all_meps = get_all_meps()
if all_meps:
    mep_options = {f"{mep['name']} ({mep['mepID']})": mep["mepID"] for mep in all_meps}
    selection = st.selectbox("Select MEP by name", list(mep_options.keys()))
    if st.button("Add Selected MEP"):
        add_to_watchlist(mep_options[selection])
else:
    st.warning("⚠️ No MEPs available.")
>>>>>>> origin/main
