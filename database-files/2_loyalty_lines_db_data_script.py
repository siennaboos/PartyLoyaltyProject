import requests

meps = requests.get('https://data.europarl.europa.eu/api/v2/meps?format=application%2Fld%2Bjson')

print(meps)