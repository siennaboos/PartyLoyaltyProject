from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import sqlite3
from backend.ml_models import new_recommender_cosine as recommender
import os

# Blueprint setup
recommender_bp = Blueprint('recommender_bp', __name__)

@recommender_bp.route('/recommender', methods=['GET'])
def recommend():
    try:
        # Validate required query parameters
        required_params = ['agree', 'attendance', 'party', 'party_pct', 'country', 'country_weight']
        missing = [p for p in required_params if request.args.get(p) is None]

        if missing:
            return jsonify({'error': f"Missing parameter(s): {', '.join(missing)}"}), 400

        # Get query parameters
        agree = float(request.args.get('agree'))
        attendance = float(request.args.get('attendance'))
        party = request.args.get('party')
        party_pct = float(request.args.get('party_pct'))
        country = request.args.get('country')
        country_weight = float(request.args.get('country_weight'))

        # Load CSV
        csv_path = os.path.join(os.getcwd(), 'backend/ml_models/active_members.csv')
        df = recommender.make_full_df(csv_path)

        # Generate weights
        weights = recommender.get_weights_vector(
            percent_agree_current_weight=5,
            percent_attendance_weight=90,
            my_party=party,
            my_party_percentage_weight=4,
            new_candidate_country_weight=country_weight
        )

        # Get top 10 recommendations
        recs_df = recommender.get_recommendations(
            df,
            agree,
            attendance,
            party,
            party_pct,
            new_candidate_country=country,
            weights=weights
        )

        return jsonify(recs_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': str(e)}), 400

csv_path = os.path.join(os.getcwd(), 'backend/ml_models/active_members.csv')
belgium_df = pd.read_csv(csv_path)


@recommender_bp.route('/get-dissenters', methods=['GET'])
def get_dissenters_route():
    party_name = request.args.get('party_name')

    if not party_name:
        return jsonify({'error': 'Missing party_name parameter'}), 400

    # Copy the DataFrame to work with
    df = belgium_df.copy()

    # 🔍 Add these lines right here — before any filtering
    print("User is searching for party name:", party_name)
    print("Available party names in dataset:", df['party'].unique())

    # Now do the filtering (optionally more flexible with str.contains)
    df = df[df['party'].str.contains(party_name, case=False, na=False)]
    df = df[df['percent_agree_current'] != 0]

    df = df[['id', 'first_name', 'last_name', 'percent_dissent_current']]
    df = df.sort_values(by='percent_dissent_current', ascending=False)
    df = df.rename(columns={
        'id': 'MEP ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'percent_dissent_current': 'Dissent Rate'
    })

    dissents = df.head(10)

    return jsonify(dissents.to_dict(orient='records'))

@recommender_bp.route('/get-dissent-rate', methods=['GET'])
def get_dissent_rate():
    """
    Returns the dissent rate for a given MEP using only their unique ID.
    Query parameters:
        - id (str or int): MEP ID
    """
    mep_id = request.args.get('id')

    if not mep_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    df = belgium_df.copy()

    # Filter by ID (convert to str in case of int/str mismatch)
    filtered = df[df['id'].astype(str) == str(mep_id)]

    if filtered.empty:
        return jsonify({'error': f'MEP with id {mep_id} not found'}), 404

    mep_data = filtered.iloc[0]
    return jsonify({
        'id': mep_id,
        'first_name': mep_data['first_name'],
        'last_name': mep_data['last_name'],
        'party': mep_data['party'],
        'dissent_rate': mep_data['percent_dissent_current']
    })