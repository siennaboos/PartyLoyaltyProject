import streamlit as st
import pandas as pd
import requests


from modules.nav import SideBarLinks
SideBarLinks()


st.title("Find Your Top 10 MEP Matches")

party_abbrevs = {
   'European People’s Party': 'EPP',
   'Renew Europe': 'RENEW',
   'Progressive Alliance of Socialists and Democrats': 'SD',
   'European Conservatives and Reformists': 'ECR',
   'Non-attached Members': 'NI',
   'Europe of Sovereign Nations': 'ESN',
   'The Left in the European Parliament – GUE/NGL': 'GUE_NGL',
   'Greens/European Free Alliance': 'GREEN_EFA',
   'Patriots for Europe': 'PFE'
}


countries_url = 'http://web-api:4000/b/mep_countries'
countries_response = requests.get(countries_url)
countries_data = countries_response.json()


countries_list = [item['country'] for item in countries_data]
countries_list.insert(0, 'Not Specified')
parties_list = ['European People’s Party', 'Renew Europe', 'Progressive Alliance of Socialists and Democrats',
   'European Conservatives and Reformists', 'Europe of Sovereign Nations',
   'The Left in the European Parliament – GUE/NGL', 'Greens/European Free Alliance',
   'Patriots for Europe']


user_party = st.selectbox('Your Party', parties_list)

route_input_party = party_abbrevs[user_party]



agree_current = st.slider("Current Party Alignment (%)", 0, 100, 40)
agree_new_party = st.slider(f'{user_party} Alignment (%)', 0, 100, 70)
attendance = st.slider("Attendance Rate (%)", 0, 100, 80)



recruit_parties = [party for party in parties_list if party != user_party]
recruit_parties.append('Non-attached Members')
recruit_parties.insert(0, 'Not Specified')
st.write('Optional Filters')


recruit_party = st.selectbox('What party are they currently in?', recruit_parties)
if recruit_party != 'Not Specified':
   recruit_party = party_abbrevs[recruit_party]


recruit_country = st.selectbox("What country are they from?", countries_list)


url = "http://web-api:4000/b/active_mep_alignment_data"
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)




weights = []


if 'weights_set' not in st.session_state:
   st.session_state.weights_set = False


if st.button('Add Feature Importance Values', type='primary'):
   st.session_state.weights_set = True


if st.session_state.weights_set:
    st.write('#### Values must add up to 100!')


    agree_current_weight = st.slider("Current Party Alignment Importance (%)", 0, 100, 50)
    weights.append(agree_current_weight)
    attendance_weight = st.slider("Attendance Rate Importance (%)", 0, 100, 50)
    weights.append(attendance_weight)
    agree_new_weight = st.slider(f"{user_party} Alignment Weight (%)", 0, 100, 50)
    weights.append(agree_new_weight)


    if recruit_party != 'Not Specified':
        party_weight = st.slider("Party Importance (%)", 0, 100, 50)
        weights.append(party_weight)
  
    if recruit_country != 'Not Specified':
        country_weight = st.slider("Country Importance (%)", 0, 100, 50)
        weights.append(country_weight)

    if sum(weights) != 100:
        st.warning('Feature Importance Values do not add up to 100')
    else:
        weights_str = str(weights).replace(" ", "")
        weights_str = weights_str[:len(weights_str)-1]


if st.button("Get Recommendations"):
    base_url = f"http://web-api:4000/b/get_recs/{agree_current}/{attendance}/{route_input_party}/{agree_new_party}"
    params = []


    if recruit_party != 'Not Specified':
        params.append(f"new_candidate_party={recruit_party}")
    if recruit_country != 'Not Specified':
        params.append(f"new_candidate_country={recruit_country}")
    if weights:
        params.append(f"weights={weights_str}")


    if params:
        query_string = "&".join(params)
        full_url = f"{base_url}?{query_string}"
    else:
        full_url = base_url


    response = requests.get(full_url)


    recruits = pd.DataFrame(response.json())
    recruits.rename(columns={f'{route_input_party} Alignment Rate': f'{user_party} Alignment Rate'}, inplace=True)
    st.dataframe(recruits.drop(columns=['mep_dot_product', 'mep_cosine']))   