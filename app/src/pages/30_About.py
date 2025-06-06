import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

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

SideBarLinks()


st.write("# About this App")


st.markdown(
    """
    This is a demo app for Data and Software in International Government and Politics Dialogue 2025 Project Course.  

    The goal of this demo is to provide information on the tech stack 
    being used as well as demo some of the features of the various platforms. 

    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
