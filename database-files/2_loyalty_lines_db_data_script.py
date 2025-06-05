import requests

meps = requests.get('https://data.europarl.europa.eu/api/v2/meps?format=application%2Fld%2Bjson&offset=0').json()
# print(meps)

for mep in meps['data']:
    mep_id = mep['id'].split("/")[1] 

    in_depth = requests.get(f'https://data.europarl.europa.eu/api/v2/meps/{mep_id}?format=application%2Fld%2Bjson').json()
    print(in_depth['data'])

    print("\n\n\n")
