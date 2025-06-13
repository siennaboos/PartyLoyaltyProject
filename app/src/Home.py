import streamlit as st
from PIL import Image
import requests

st.set_page_config(layout="wide")

# CSS Styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'sans-serif' !important;
        background-color: #f0f4fb;
    }
    .block-container {
        padding: 3rem 5rem;
    }
    .stButton>button {
        background-color: #365fc7;
        color: white;
        padding: 0.6em 1.5em;
        border-radius: 8px;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .stButton>button:hover {
        background-color: #2e4da5;
    }
    </style>
""", unsafe_allow_html=True)
from modules.nav import SideBarLinks


@st.cache_data
def get_all_party_leaders():

    response = requests.get("http://web-api:4000/u/users/role/1")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users



@st.cache_data
def get_all_political_journalists():
    response = requests.get("http://web-api:4000/u/users/role/2")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users


@st.cache_data
def get_all_citizens():
    response = requests.get("http://web-api:4000/u/users/role/3")
    if response.status_code != 200:
        st.error("Failed to access users")
        st.stop()


    users = response.json()

    return users

SideBarLinks()


pls = get_all_party_leaders()
pjs = get_all_political_journalists()
czs = get_all_citizens()


st.write(pls)
st.write(pjs)
st.write(czs)



# Hero Section Layout
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("## **Welcome to Loyalty Lines**")
    st.markdown("*Track EU votes. Understand MEP loyalty.*")

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