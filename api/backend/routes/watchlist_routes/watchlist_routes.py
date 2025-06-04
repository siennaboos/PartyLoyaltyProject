from flask import Blueprint, request, jsonify, current_app, make_response

from backend.db_connection import db

watchlists = Blueprint("watchlists", __name__)

@watchlists.route("/user/<int:userID>/watchlists", methods=['GET'])
def get_all_users_watchlists(userID):
    current_app.logger.info('GET /user/<userID>/watchlists route entered')
    query = '''
        SELECT 
        FROM user;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()
    
    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response