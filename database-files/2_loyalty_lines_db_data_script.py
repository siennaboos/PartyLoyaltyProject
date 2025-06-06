# import requests

# meps = requests.get('https://data.europarl.europa.eu/api/v2/meps?format=application%2Fld%2Bjson&offset=0')
# # print(meps)

# try:
#     meps = meps.json()
# except ValueError:
#     print("bad")
#     print(meps.text[:500])


# print(f"retrieved {len(meps['data'])}MEPs")

# for mep in meps['data']:
#     mep_id = mep['id'].split("/")[1] 

#     in_depth = requests.get(f'https://data.europarl.europa.eu/api/v2/meps/{mep_id}?format=application%2Fld%2Bjson').json()
#     mep_specifics = in_depth['data'][0]

    
#     print("rerieved in depth info")
#     eu_group_id = None

#     for membership in mep_specifics["hasMembership"]:
#         if membership.get("membershipClassification") == "def/ep-entities/EU_POLITICAL_GROUP":
#             eu_group_id = membership.get("organization")
#             break

    


#     print("\n\n\n")

# # @app.route("/meps")
# # def getMEPs():
# #     try:
# #         resp = requests.get("https://data.europarl.europa.eu/api/v2/meps", headers=HEADERS)
# #         data = resp.json()

# #         meps_raw = data.get("data", [])
# #         mep_records = []

# #         for mep in meps_raw:
# #             if not isinstance(mep, dict):
# #                 continue

# #             mep_id_raw = mep.get("id", "")
# #             mep_id = mep_id_raw.split("/")[-1]
# #             name = mep.get("label", "")
# #             european_group = mep.get("politicalGroup", {}).get("label", "") 

# #             if mep_id and name:
# #                 mep_records.append({
# #                     "mep_id": mep_id,
# #                     "name": name,
# #                     "country": country_of_representation
# #                     "european_group": european_group
# #                 })

# #         meps_df = pd.DataFrame(mep_records)
# #         meps_df.to_csv("meps_ref.csv", index=False)

# #         return jsonify(mep_records)