import logging
logger = logging.getLogger(__name__)

import streamlit as st
from PIL import Image
import time

from modules.nav import SideBarLinks

# Set layout to wide
st.set_page_config(layout="wide")

# Show appropriate sidebar links for the current user
SideBarLinks()

# --- Add CSS for blue buttons ---
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #3366cc;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #264d99;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Typewriter animation function ---
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(
            f"<h1 style='text-align: left; font-size: 48px;'>{curr_full_text}</h1>",
            unsafe_allow_html=True
        )
        time.sleep(1 / speed)

# --- Hero Section Layout ---
left, right = st.columns([2, 1], gap="large")

with left:
    # Title with typewriter effect
    typewriter("Welcome to Loyalty Lines", speed=20)

    # Subtitle
    st.markdown(
        "<p style='font-size: 20px; font-style: italic;'>Track EU votes. Understand MEP loyalty.</p>",
        unsafe_allow_html=True
    )

    # Navigation buttons
    if st.button("Γιάννη Πούλος (Party Leader)", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'party_leader'
        st.session_state['first_name'] = 'Yanni'
        st.switch_page("pages/00_Party_Leader_Home.py")

    if st.button("Camila Romero (Journalist)", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'political_journalist'
        st.session_state['first_name'] = 'Camila'
        st.switch_page("pages/10_Political_Journalist_Home.py")

    if st.button("Greg Gerborg (Citizen)", use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'citizen'
        st.session_state['first_name'] = 'Greg'
        st.switch_page("pages/20_Citizen_Home.py")

with right:
    st.image("assets/blogo.png", width=400)