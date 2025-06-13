from flask import Blueprint, request, jsonify, current_app, make_response
from mysql.connector import Error

from backend.db_connection import db

watchlists = Blueprint("watchlists", __name__)

# Returns all of the MEPs in the user's watchlist 
@watchlists.route("/user/<int:userID>/watchlists", methods=['GET'])
def get_all_users_watchlists(userID):
    current_app.logger.info('GET /user/<userID>/watchlists route entered')
    query = '''
        SELECT mep.mepID, name, countryOfOrigin, loyaltyScore, partyID, recommendedPartyID, photoURL
        FROM mep 
        JOIN watchList as wl ON mep.mepID = wl.mepID
        WHERE wl.userID = %s
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query, (userID))
    retrieved_users = cursor.fetchall()
    cursor.close()
    
    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response


@watchlists.route("/user/<int:userID>/watchlists", methods=['POST'])
def add_user_to_watchlist(userID):
    current_app.logger.info('POST /user/<userID>/watchlists route entered')

    try:
        data = request.json

        required_fields = ["mepID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO watchList (mepID, userID)
            VALUES (%s, %s);
        """

        cursor.execute(query, (data['mepID'], userID))
    
        db.get_db().commit()
        cursor.close()
        
        return (jsonify({"message": "MEP added successfully", "mepID": data["mepID"]}), 201,)
        
    except Error as e:
        return jsonify({"error": str(e)}), 500


@watchlists.route("/user/<int:userID>/watchlists", methods=['DELETE'])
def remove_mep_from_watchlist(userID):
    current_app.logger.info('DELETE /user/<userID>/watchlists route entered')

    try:
        data = request.json

        required_fields = ["mepID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400


        cursor = db.get_db().cursor()

        query = """
            DELETE FROM watchList
            WHERE mepID = %s
              AND userID = %s;
        """
        cursor.execute(query, (data["mepID"], userID))

        db.get_db().commit()
        cursor.close()

        return (jsonify({"message":  "MEP removed successfully", "mepID": data['mepID']}), 200,)

    except Error as e:
        return jsonify({"error": str(e)}), 500