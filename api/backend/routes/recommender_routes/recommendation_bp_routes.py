from flask import Blueprint, jsonify, current_app, make_response, request
import pandas as pd
import io
import numpy as np
import sqlite3
import backend.ml_models.new_recommender_cosine as recommender
import os
from mysql.connector import Error


from backend.db_connection import db


# Blueprint setup
recommender_bp = Blueprint('recommender_bp', __name__)


@recommender_bp.route('/mep_countries', methods=['GET'])
def mep_countries():
   current_app.logger.info('GET /countries route entered')
   query = '''
       SELECT DISTINCT country
       FROM recommender_input;
   '''
   cursor = db.get_db().cursor()


   cursor.execute(query)
   retrieved_countries = cursor.fetchall()
   cursor.close()


   current_app.logger.info("GET /countries route success")
   response = make_response(jsonify(retrieved_countries))
   response.status_code = 200
  
   return response


@recommender_bp.route('/active_mep_alignment_data', methods=['GET'])
def active_mep_alignment_data():
   current_app.logger.info('GET /alignment data route entered')
   query = '''
       SELECT *
       FROM recommender_input;
   '''
   cursor = db.get_db().cursor()
   cursor.execute(query)


   retrieved_alignment_data = cursor.fetchall()

   data = []


   for row in retrieved_alignment_data:
       result = {'id': row['id'],
                 'first_name': row['first_name'],
                 'last_name': row['last_name'],
                 'party': row['party'],
                 'party_code': row['party_code'],
                 'agreed': row['agreed'],
                 'dissented': row['dissented'],
                 'did_not_vote': row['did_not_vote'],
                 'total_votes': row['total_votes'],
                 'real_vote_count': row['real_vote_count'],
                 'percent_agree_current': row['percent_agree_current'],
                 'percent_dissent_current': row['percent_dissent_current'],
                 'percent_show_up': row['percent_show_up'],
                 'country': row['country'],
                 'European People’s Party percentage': row['EuropeanPeoplesPartypercentage'],
                 'Renew Europe percentage': row['RenewEuropepercentage'],
                 'Progressive Alliance of Socialists and Democrats percentage': row['ProgressiveAllianceofSocialistsandDemocratspercentage'],
                 'European Conservatives and Reformists percentage': row['EuropeanConservativesandReformistspercentage'],
                 'Non-attached Members percentage': row['Non_attachedMemberspercentage'],
                 'Europe of Sovereign Nations percentage': row['EuropeofSovereignNationspercentage'],
                 'The Left in the European Parliament – GUE/NGL percentage': row['TheLeftintheEuropeanParliament_GUE_NGLpercentage'],
                 'Greens/European Free Alliance percentage': row['Greens_EuropeanFreeAlliancepercentage'],
                 'Patriots for Europe percentage': row['PatriotsforEuropepercentage'],
                 'Identity and Democracy percentage': row['IdentityandDemocracypercentage']}


       data.append(result)


   current_app.logger.info("GET /alignment data route success")
   response = make_response(jsonify(data))
   response.status_code = 200
  
   return response


@recommender_bp.route('/get_recs/<int:percent_agree_current>/<int:percent_attendance>/<my_party>/<int:my_party_percentage>', methods = ['GET'])
def get_recs(percent_agree_current, percent_attendance, my_party, my_party_percentage):
    current_app.logger.info('GET /alignment data route entered')
    query = '''
        SELECT *
        FROM recommender_input;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)


    retrieved_alignment_data = cursor.fetchall()

    data = []
  
    for row in retrieved_alignment_data:
        result = {'id': int(row['id']),
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'party': row['party'],
                'party_code': row['party_code'],
                'agreed': int(row['agreed']),
                'dissented': int(row['dissented']),
                'did_not_vote': int(row['did_not_vote']),
                'total_votes': int(row['total_votes']),
                'real_vote_count': int(row['real_vote_count']),
                'percent_agree_current': float(row['percent_agree_current']),
                'percent_dissent_current': float(row['percent_dissent_current']),
                'percent_show_up': float(row['percent_show_up']),
                'country': row['country'],
                'EPP percentage': float(row['EuropeanPeoplesPartypercentage']),
                'RENEW percentage': float(row['RenewEuropepercentage']),
                'SD percentage': float(row['ProgressiveAllianceofSocialistsandDemocratspercentage']),
                'ECR percentage': float(row['EuropeanConservativesandReformistspercentage']),
                'NI percentage': float(row['Non_attachedMemberspercentage']),
                'ESN percentage': float(row['EuropeofSovereignNationspercentage']),
                'GUE_NGL percentage': float(row['TheLeftintheEuropeanParliament_GUE_NGLpercentage']),
                'GREEN_EFA percentage': float(row['Greens_EuropeanFreeAlliancepercentage']),
                'PFE percentage': float(row['PatriotsforEuropepercentage'])}


        data.append(result)


    df = pd.DataFrame(data)


    new_candidate_party = request.args.get('new_candidate_party')
    new_candidate_country = request.args.get('new_candidate_country')
    weights = request.args.get('weights')

    if weights != None and isinstance(weights, str):
        weights = eval(weights) if weights.startswith('[') else list(map(float, weights.split(',')))



    if new_candidate_party != None and new_candidate_country != None:
        recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = new_candidate_party, new_candidate_country = new_candidate_country)
        if weights != None:
            recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = new_candidate_party, new_candidate_country = new_candidate_country, weights = weights)
  
    if new_candidate_party != None:
        recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = new_candidate_party)
        if weights != None:
            recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_party = new_candidate_party, weights = weights)


    elif new_candidate_country != None:
        recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_country = new_candidate_country)
        if weights != None:
            recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage, new_candidate_country = new_candidate_country, weights = weights)
  
    else:
        recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage = my_party_percentage)
        if weights != None:
            recruits = recommender.get_recommendations(df, percent_agree_current, percent_attendance, my_party, my_party_percentage = my_party_percentage, weights = weights)

    recruits_json = recruits.to_json(orient='records')
    return recruits_json




# starting routes
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
