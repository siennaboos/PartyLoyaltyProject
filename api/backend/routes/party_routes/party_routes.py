from flask import Blueprint, jsonify, request, current_app, make_response

from backend.db_connection import db

parties = Blueprint("parties", __name__)

@parties.route("/parties", methods=["GET"])
def get_all_parties():
    current_app.logger.info('GET /parties route entered')
    query = '''
        SELECT partyID, partyCohesionScore, partyName
        FROM political_party
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_parties = cursor.fetchall()

    current_app.logger.info("GET /parties route success")
    response = make_response(jsonify(retrieved_parties))
    response.status_code = 200
    
    return response

@parties.route("/parties/<int:partyID>")
def get_party(partyID):
    current_app.logger.info('GET /party/<int:partyID> route entered')
    query = '''
        SELECT partyID, partyCohesionScore, partyName
        FROM political_party
        WHERE paryID = %s
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (partyID))
    retrieved_party = cursor.fetchone()

    current_app.logger.info("GET /party/<int:partyID> route success")
    response = make_response(jsonify(retrieved_party))
    response.status_code = 200
    
    return response
