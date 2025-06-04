from flask import Blueprint, jsonify, current_app, make_response

from backend.db_connection import db

meps = Blueprint("meps", __name__)

@meps.route("/meps", methods=['GET'])
def get_all_meps():
    current_app.logger.info('GET /meps route entered')
    query = '''
        SELECT mepID, name, countryOfOrigin, loyaltyScore, partyID, recomendedPartyID
        FROM user;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()

    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response

@meps.route("/meps/<int:mepID>", methods=['GET'])
def get_mep(mepID):
    current_app.logger.info('GET /mep/<int:mepID> route entered')
    query = '''
        SELECT mepID, name, countryOfOrigin, loyaltyScore, partyID, recommendedPartyID, photoURL
        FROM mep
        WHERE mepID = %s;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_mep = cursor.fetchone()

    current_app.logger.info("GET /mep/<int:mepID> route success")
    response = make_response(jsonify(retrieved_mep))
    response.status_code = 200
    
    return response


@meps.route("/mep/<int:mepID>/score", methods=['GET'])
def get_mep_loyalty_score(mepID):
    current_app.logger.info('GET /mep/<int:mepID>/score route entered')
    query = '''
        SELECT loyaltyScore
        FROM mep
        WHERE mepID = mepID;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_mep = cursor.fetchone()

    current_app.logger.info("GET /mep/<int:mepID>/score route success")
    response = make_response(jsonify(retrieved_mep))
    response.status_code = 200
    
    return response


@meps.route("/mep/<int:mepID>/party", methods=['GET'])
def get_mep_party(mepID):
    current_app.logger.info('GET /mep/<int:mepID>/party route entered')
    query = '''
        SELECT partyID, partyName 
        FROM mep 
        JOIN poliical_party as p ON mep.partyID = p.partyID
        WHERE mepID = mepID;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_mep_party = cursor.fetchone()

    current_app.logger.info("GET /mep/<int:mepID>/party route success")
    response = make_response(jsonify(retrieved_mep_party))
    response.status_code = 200
    
    return response


@meps.route("/mep/<int:mepID>/picture", methods=['GET'])
def get_mep_photo(mepID):
    current_app.logger.info('GET /mep/<int:mepID>/picture route entered')
    query = '''
        SELECT photoURL 
        FROM mep 
        WHERE mepID = mepID;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_photo = cursor.fetchone()

    current_app.logger.info("GET /mep/<int:mepID>/picture route success")
    response = make_response(jsonify(retrieved_photo))
    response.status_code = 200
    
    return response

   


