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
