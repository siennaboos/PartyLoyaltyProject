import streamlit as st
import requests
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import plotly.express as px

SideBarLinks()

st.title("🧠 Party Dissent Predictor")
st.markdown("Use logistic regression to estimate dissent likelihood for EU parties.")

# --- Inputs ---
party = st.selectbox("Select a political party:", [
    'EPP', 'ESN', 'GUE/NGL', 'Greens/EFA', 'ID',
    'Patriots for Europe', 'Renew', 'S&D'
])

<<<<<<< HEAD
st.title("📈 Party Cohesion Monitor")
st.markdown("### _Track how party loyalty has changed over time._")
st.markdown("This vizualization shows how the percent of dissenters has changed for each party as time has passed.")
st.markdown("Time is measured by week index, which refers to the week in which the vote occurred chronologically relative to other votes in the available data.")
st.markdown("The data in this graph is from 2021 - 2025. Week 1 is the least recent.")

st.markdown(" ")
st.markdown("_Click party names in the legend to add/remove them from the plot._")

resp = requests.get("http://web-api:4000/t/time")
time_resp = resp.json() if resp.status_code == 200 else []

# ----------------------------
# Build DataFrame with time info
# ----------------------------
time_df = pd.DataFrame([{
    "Week Index": int(row["adjusted_week"]),
    "Party": row["party"],
    "Percent Dissent": float(row["percent_dissent"])} for row in time_resp])


avg_df = time_df.groupby(["Week Index", "Party"], as_index=False)["Percent Dissent"].mean()

fig = px.line(
    avg_df,
    x="Week Index",
    y="Percent Dissent",
    color="Party",
    title="Average Party Dissent Per Week",
    labels={"Week Index": "Week", "Percent Dissent": "Average Percent Dissent"}
)

st.plotly_chart(fig, use_container_width=True)
=======
procedure_type = st.selectbox("Select a procedure type:", [
    'APP', 'BUD', 'BUI', 'CNS', 'COD', 'DEA', 'DEC', 'INI',
    'INL', 'NLE', 'REG', 'RPS', 'RSO', 'RSP'
])

# --- Predict button ---
if st.button("🔍 Predict Dissent Rate"):
    url = f"http://web-api:4000/l/prediction/{party}/{procedure_type}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.success(f"📊 Predicted Dissent Rate: **{data['prediction']:.2f}%**")
        else:
            st.error("❌ Prediction failed. Try again or check the server.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
>>>>>>> origin/main
