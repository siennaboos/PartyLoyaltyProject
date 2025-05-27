##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit and supporting libraries
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Streamlit layout config
st.set_page_config(layout='wide')

# Assume user is unauthenticated at start
st.session_state['authenticated'] = False

# Sidebar navigation setup
from modules.nav import SideBarLinks
SideBarLinks(show_home=True)

# ***************************************************
# LOGIN SECTION — your original code (kept exactly)
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('European Parliament Party Loyalty and Cohesion Analysis')
st.write('\n\n')
st.write('### 2025 Summer 1 Dialogue of Civilizations')
st.write('\n')
st.write('#### HI! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as John, a Political Strategy Advisor", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'pol_strat_advisor'
    st.session_state['first_name'] = 'John'
    logger.info("Logging in as Political Strategy Advisor Persona")
    st.switch_page('pages/00_Pol_Strat_Home.py')

if st.button('Act as Mohammad, an USAID worker', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'usaid_worker'
    st.session_state['first_name'] = 'Mohammad'
    st.switch_page('pages/10_USAID_Worker_Home.py')

if st.button('Act as System Administrator', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'SysAdmin'
    st.switch_page('pages/20_Admin_Home.py')

# ***************************************************
# GRAPH SECTION — new addition below login UI
# ***************************************************

st.divider()
st.subheader("📊 Preview: MEP Loyalty Scoreboard")

try:
    response = requests.get("http://localhost:5001/loyalty")
    response.raise_for_status()
    data = response.json()

    loyalty_df = pd.DataFrame(data["loyalty_scores"])

    fig = px.bar(
        loyalty_df.sort_values("Loyalty_Score", ascending=False),
        x="MEP", y="Loyalty_Score", title="Loyalty to European Party (%)",
        color="Loyalty_Score", color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning(f"Loyalty data could not be loaded: {e}")