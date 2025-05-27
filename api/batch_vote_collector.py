import requests
import pandas as pd
import os
import time

def fetch_votes_list():
    url = "https://howtheyvote.eu/api/votes?limit=100"
    resp = requests.get(url)
    return [v["id"] for v in resp.json()["votes"]]

def process_vote(vote_id):
    url = f"https://howtheyvote.eu/api/votes/{vote_id}"
    resp = requests.get(url)
    data = resp.json()

    if "votes" not in data or not data["votes"]:
        return None, None, None  # Skip votes without detailed data

    vote_records = []
    mep_records = []

    for v in data["votes"]:
        mep = v.get("mep", {})
        vote_option = v.get("option", "Unknown")

        vote_records.append({
            "mep_id": mep.get("id"),
            "vote_id": vote_id,
            "individual_vote": vote_option
        })

        mep_records.append({
            "mep_id": mep.get("id"),
            "mep_name": f"{mep.get('first_name', '')} {mep.get('last_name', '')}".strip(),
            "country": mep.get("country", "Unknown"),
            "national_party": mep.get("national_party", {}).get("name", "Unknown"),
            "european_group": mep.get("group", {}).get("name", "Unknown")
        })

    votes_df = pd.DataFrame(vote_records)
    meps_df = pd.DataFrame(mep_records).drop_duplicates("mep_id")

    combined = pd.merge(votes_df, meps_df, on="mep_id", how="left")
    group_summary_df = (
        combined.groupby(["european_group", "vote_id"])["individual_vote"]
        .agg(lambda x: x.value_counts().idxmax())
        .reset_index()
        .rename(columns={"individual_vote": "group_majority_vote"})
    )

    return meps_df, votes_df, group_summary_df

def save_to_csv(meps_df, votes_df, group_df, vote_id):
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    meps_df.to_csv(f"{out_dir}/meps_{vote_id}.csv", index=False)
    votes_df.to_csv(f"{out_dir}/votes_{vote_id}.csv", index=False)
    group_df.to_csv(f"{out_dir}/group_summary_{vote_id}.csv", index=False)

def run_batch(limit=5):
    vote_ids = fetch_votes_list()
    count = 0

    for vote_id in vote_ids:
        print(f"Processing vote {vote_id}...")
        meps_df, votes_df, group_summary_df = process_vote(vote_id)

        if meps_df is not None:
            save_to_csv(meps_df, votes_df, group_summary_df, vote_id)
            print(f"✅ Saved vote {vote_id}")
            count += 1

        if count >= limit:
            break

        time.sleep(1)  # avoid overloading the API

if __name__ == "__main__":
    run_batch(limit=5)