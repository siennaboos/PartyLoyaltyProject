from flask import Flask
import requests

app = Flask(__name__)

API_URL = "https://data.europarl.europa.eu/api/v2/meps"
HEADERS   = {"accept": "application/ld+json"}



@app.route("/meps")
def getMEPs():
    try:

        params = {
            "format": "application/ld+json",
        }

        resp = requests.get("https://data.europarl.europa.eu/api/v2/meps", params, headers=HEADERS)
        print(resp)
        data = resp.json()  
        return data

    except requests.exceptions.RequestException as e:
        print("failed:", e)
        return "bad"


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
    

@app.route("/voteEU/<int:vote_id>")
def getVoteEU(vote_id):
    try:

        params = {
            "format": "application/ld+json",
        }

        resp = requests.get(f"https://howtheyvote.eu/api/votes/{vote_id}", params=params, headers=HEADERS)
        print(resp)
        data = resp.json()  
        return data

    except requests.exceptions.RequestException as e:
        print("failed:", e)
        return "bad"
    


if __name__ == "__main__":
    app.run(debug=True)

