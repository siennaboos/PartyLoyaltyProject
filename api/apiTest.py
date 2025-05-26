from flask import Flask, jsonify
import requests
import pandas as pd
from process_votes import fetch_and_process_vote_data

app = Flask(__name__)

API_URL = "https://data.europarl.europa.eu/api/v2/meps"
HEADERS   = {"accept": "application/ld+json"}

app = Flask(__name__)

@app.route("/meps")
def getMEPs():
    try:
        resp = requests.get("https://data.europarl.europa.eu/api/v2/meps", headers=HEADERS)
        data = resp.json()

        meps_raw = data.get("data", [])
        mep_records = []

        for mep in meps_raw:
            if not isinstance(mep, dict):
                continue

            mep_id_raw = mep.get("id", "")
            mep_id = mep_id_raw.split("/")[-1]
            name = mep.get("label", "")
            european_group = mep.get("politicalGroup", {}).get("label", "")  # ✅ group added

            if mep_id and name:
                mep_records.append({
                    "mep_id": mep_id,
                    "name": name,
                    "european_group": european_group
                })

        meps_df = pd.DataFrame(mep_records)

        import os
        os.makedirs("output", exist_ok=True)
        meps_df.to_csv("output/meps_list.csv", index=False)

        return jsonify(mep_records)

    except Exception as e:
        print("Error fetching MEPs:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/voteEU")
def getEUs():
    try:

        params = {
            "format": "application/ld+json",
        }

        resp = requests.get("https://howtheyvote.eu/api/votes", params, headers=HEADERS)
        print(resp)
        data = resp.json()  
        return data

    except requests.exceptions.RequestException as e:
        print("failed:", e)
        return "bad"
    

@app.route("/votes/<int:vote_id>")
def getVotes(vote_id):
    try:
        # Call HowTheyVote.eu API
        url = f"https://howtheyvote.eu/api/votes/{vote_id}"
        resp = requests.get(url)
        data = resp.json()

        if "votes" not in data or not data["votes"]:
            return jsonify({"error": "No individual votes available for this vote_id"}), 404

        vote_records = []

        for vote_entry in data["votes"]:
            mep = vote_entry.get("mep", {})
            mep_id_raw = mep.get("id", "")
            mep_id = mep_id_raw.split("/")[-1]  # Extract ID number from "person/123"
            vote_option = vote_entry.get("option", "Unknown")

            if mep_id and vote_option:
                vote_records.append({
                    "mep_id": mep_id,
                    "vote_id": vote_id,
                    "individual_vote": vote_option
                })

        votes_df = pd.DataFrame(vote_records)

        # Save to CSV
        import os
        os.makedirs("output", exist_ok=True)
        votes_df.to_csv(f"output/votes_{vote_id}.csv", index=False)

        return jsonify(vote_records)

    except Exception as e:
        print("Error in /votes route:", e)
        return jsonify({"error": str(e)}), 500
    


import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os
from flask import jsonify

@app.route("/votes_real")
def get_real_votes():
    try:
        # Get the first real vote from RegData
        index_url = "https://www.europarl.europa.eu/RegData/rcv/rcv.json"
        index_resp = requests.get(index_url)
        index_data = index_resp.json()

        # Grab first vote w/ XML
        first_vote = index_data["rcvs"][0]
        xml_url = first_vote["rollCallDataUrl"]
        vote_id = first_vote["documentCode"]

        # Parse XML vote file
        xml_resp = requests.get(xml_url)
        root = ET.fromstring(xml_resp.content)

        votes = []
        for vote in root.findall(".//vote"):
            name = vote.get("name")
            vote_value = vote.get("value")
            if name and vote_value:
                votes.append({
                    "name": name.strip(),
                    "vote_id": vote_id,
                    "individual_vote": vote_value.strip()
                })

        votes_df = pd.DataFrame(votes)

        # ✅ Save the real vote file
        os.makedirs("output", exist_ok=True)
        votes_df.to_csv("output/votes_real.csv", index=False)

        return jsonify(votes_df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)