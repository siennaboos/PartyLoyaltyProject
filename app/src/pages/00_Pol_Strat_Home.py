import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# Inject global CSS for font override
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

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Party Leader, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Party Recruitment Dashboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Party_Recommend.py')

if st.button('Party Cohesion Over Time', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Cohesion_Monitor.py')