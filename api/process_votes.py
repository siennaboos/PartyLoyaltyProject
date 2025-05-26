import requests
import pandas as pd
import os

def fetch_and_process_vote_data(vote_id):
    vote_url = f"https://howtheyvote.eu/api/votes/{vote_id}"
    vote_resp = requests.get(vote_url)
    vote_data = vote_resp.json()

    vote_records = []
    mep_records = []

    for v in vote_data.get("votes", []):
        mep_info = v.get("mep", {})
        vote_option = v.get("option", "Unknown")

        vote_records.append({
            "mep_id": mep_info.get("id"),
            "vote_id": vote_id,
            "individual_vote": vote_option
        })

        mep_records.append({
            "mep_id": mep_info.get("id"),
            "mep_name": f"{mep_info.get('first_name', '')} {mep_info.get('last_name', '')}".strip(),
            "country": mep_info.get("country", "Unknown"),
            "national_party": mep_info.get("national_party", {}).get("name", "Unknown"),
            "european_group": mep_info.get("group", {}).get("name", "Unknown")
        })

    votes_df = pd.DataFrame(vote_records)
    meps_df = pd.DataFrame(mep_records).drop_duplicates("mep_id")

    if not meps_df.empty and not votes_df.empty:
        combined_df = pd.merge(votes_df, meps_df, on="mep_id")
        group_summary_df = (
            combined_df.groupby(["european_group", "vote_id"])["individual_vote"]
            .agg(lambda x: x.value_counts().idxmax())
            .reset_index()
            .rename(columns={"individual_vote": "group_majority_vote"})
        )
    else:
        group_summary_df = pd.DataFrame(columns=["european_group", "vote_id", "group_majority_vote"])

    # ✅ Save to CSV
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    meps_df.to_csv(f"{output_dir}/meps_{vote_id}.csv", index=False)
    votes_df.to_csv(f"{output_dir}/votes_{vote_id}.csv", index=False)
    group_summary_df.to_csv(f"{output_dir}/group_summary_{vote_id}.csv", index=False)

    return meps_df, votes_df, group_summary_df