from flask import Blueprint, jsonify, current_app, make_response

from backend.db_connection import db

meps = Blueprint("meps", __name__)

@meps.route("/meps", methods=['GET'])
def get_meps():
    current_app.logger.info('GET /meps route entered')
    query = '''
        SELECT mepID, name, countryOfOrigin, partyID, recomendedPartyid
        FROM user
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()

    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response

