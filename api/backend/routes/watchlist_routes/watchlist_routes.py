from flask import Blueprint, request, jsonify, current_app, make_response
from mysql.connector import Error

from backend.db_connection import db

watchlists = Blueprint("watchlists", __name__)

# Returns all of the MEPs in the user's watchlist 
@watchlists.route("/user/<int:userID>/watchlists", methods=['GET'])
def get_all_users_watchlists(userID):
    current_app.logger.info('GET /user/<userID>/watchlists route entered')
    query = '''
        SELECT watchListID, mepID, name, countryOfOrigin, loyaltyScore, partyID, recommendedPartyID
        FROM user 
        JOIN mepToWatchList as mtl ON user.watchListID = mtl.watchListID
        JOIN mep ON mep.mepID = mtl.mepID
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()
    cursor.close()
    
    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response


@watchlists.route("/user/<int:userID>/watchlists", method=['POST'])
def add_user_to_watchlist(userID):
    current_app.logger.info('POST /user/<userID>/watchlists route entered')

    try:
        data = request.json

        required_fields = ["mepID", "watchListID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO mepToWatchList (watchListID, mepID)
            VALUES (%s, %s);
        """

        cursor.execute(query, (data['mepID'], data['watchListID']))
    
        db.get_db().commit()
        cursor.close()
        
        return (jsonify({"message": "MEP added successfully", "mepID": data["mepID"]}), 201,)
        
    except Error as e:
        return jsonify({"error": str(e)}), 500


@watchlists.route("/user/<int:mepID>/watchlists", method=['DELETE'])
def remove_mep_from_watchlist(mepID):
    current_app.logger.info('DELETE /user/<mepID>/watchlists route entered')

    try:
        data = request.json

        required_fields = ["watchListID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            DELETE FROM mepToWatchList
            WHERE watchListID = %s
              AND mepID = %s;
        """
        cursor.execute(query, (data["watchListID"], mepID))

        db.get_db().commit()
        cursor.close()

        return (jsonify({"message":  "MEP removed successfully", "mepID": mepID,"watchListID": data["watchListID"]}), 200,)

    except Error as e:
        return jsonify({"error": str(e)}), 500