import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

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

st.title(f"Welcome Political Journalist, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('MEP Party Loyalty Records', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_MEP_Loyalty_Records.py')

if st.button('Party Cohesion Monitor', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Party_Cohesion_Monitor.py')

if st.button("Party Recommender",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Recommender.py')
  