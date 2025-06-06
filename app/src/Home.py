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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")  


# Assume user is unauthenticated at start
st.session_state['authenticated'] = False

# Sidebar navigation setup
from modules.nav import SideBarLinks
SideBarLinks(show_home=True)


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

# ***************************************************
# LOGIN SECTION — your original code (kept exactly)
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('Loyalty Lines')
st.write('## European Parliament Party Loyalty and Cohesion Analysis')
st.write('\n\n')
st.write('#### HI! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Γιάννη Πούλος (Yanni Poulos), a Party Leader", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'party_leader'
    st.session_state['first_name'] = 'Yanni'
    logger.info("Logging in as Party Leader Persona")
    st.switch_page('pages/00_Party_Leader_Home.py')

if st.button('Act as Camila Romero, a Political Journalist', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'political_journalist'
    st.session_state['first_name'] = 'Camila'
    logger.info("Logging in as the Political Journalist")
    st.switch_page('pages/10_Political_Journalist_Home.py')

if st.button('Act as Greg Gerborg, a Citizen', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'citizen'
    st.session_state['first_name'] = 'Greg'
    logger.info("Logging in as a citizen")
    st.switch_page('pages/20_Citizen_Home.py')

# ***************************************************
# GRAPH SECTION — new addition below login UI
# ***************************************************

st.divider()
st.subheader("📊 Preview: MEP Loyalty Scoreboard")


# Dummy party seat counts — update dynamically from CSV in production
party_seats = {
    'EPP': 188,
    'S&D': 136,
    'Renew Europe': 77,
    'Greens/EFA': 53,
    'The Left': 46,
    'Patriots for Europe': 84,
    'ECR': 78,
    'ESN': 25,
    'NI': 33
}


# Color mapping 
party_colors = {
    'EPP': '#0056A0',
    'S&D': '#E60000',
    'Renew Europe': '#009fe3',
    'Greens/EFA': '#54B948',
    'The Left': '#A10000',
    'Patriots for Europe': '#666666',
    'ECR': '#003366',
    'ESN': '#888888',
    'NI': '#444444'
}


st.title("European Parliament Majority Builder")

# Checkbox controls
st.write("### Select political groups to include in the coalition:")
selected_parties = []
cols = st.columns(3)
for i, (party, seats) in enumerate(party_seats.items()):
    with cols[i % 3]:
        if st.checkbox(f"{party} ({seats})", value=True):
            selected_parties.append(party)

# Calculate selected and total seats
selected_seats = sum(party_seats[p] for p in selected_parties)
total_seats = sum(party_seats.values())
missing = max(0, 361 - selected_seats)


labels = selected_parties + ["Remaining"]

values = [party_seats[p] for p in selected_parties] + [total_seats]
colors = [party_colors[p] for p in selected_parties] + ['rgba(0,0,0,0)']  # transparent

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    direction='clockwise',
    sort=False,
    textinfo='none',
    marker=dict(colors=colors),
    showlegend=False
)])


fig.update_traces(rotation=270)  
fig.update_layout(
    height=600,
    width=800,
    margin=dict(t=10, b=10, l=10, r=10),
    annotations=[
        dict(text=f"{selected_seats} / 720<br>Seats", x=0.5, y=0.5, font_size=20, showarrow=False),
        dict(text=f"{missing} missing for<br>absolute majority", x=0.5, y=0.05, font_size=14, showarrow=False)
    ]
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.write("According to Parliament's rules, a political group shall consist of at least 23 Members elected in at least seven Member States.")