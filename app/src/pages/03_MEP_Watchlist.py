import plotly.graph_objects as go
import streamlit as st
import requests

from modules.nav import SideBarLinks
SideBarLinks()

@st.cache_data
def get_watchList_data():
    # Load MEPs
    response = requests.get("http://web-api:4000/w/user/")
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

st.title("📊 MEP Watchlist")
st.markdown("Track dissent and alignment across EU parties with visual insights.")


