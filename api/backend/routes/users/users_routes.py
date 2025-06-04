from flask import Blueprint, request, jsonify, current_app, make_response

from backend.db_connection import db

users = Blueprint("users", __name__)

@users.route("/users", methods=["GET"])
def get_users():
    
    current_app.logger.info('GET /users route entered')
    query = '''
        SELECT userID, age, countryOfOrigin, firstName, lastName, partyID, watchListID, userRole
        FROM user;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()
    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response



@users.route("/user", methods=["POST"])
def create_user():
    current_app.logger.info('POST /users route entered')
    user_data = request.json


    age = user_data['age']
    countryOfOrigin = user_data['countryOfOrigin']
    firstName = user_data['firstName']
    lastName = user_data['lastName']
    partyID = user_data['partyID']
    userRole = user_data['userRole']

    params = (age, countryOfOrigin, firstName, lastName, partyID, userRole)

    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO user (age, countryOfOrigin, firstName, lastName, partyID, userRole)
        VALUES (%s, %s, %s, %s, %s, %s);
    '''

    cursor.execute(query, params)
    db.get_db().commit()

    current_app.logger.info('POST /users route success')

    response = make_response(jsonify({'message': 'User created successfully', 'userID': cursor.lastrowid}))
    response.status_code = 200
    cursor.close()
    return response


@users.route("/user/<int:userID>", methods=["GET"])
def get_user(userID):
    current_app.logger.info("GET /user/<int:userID> route entered")

    query = '''
        SELECT userID, age, countryOfOrigin, firstName, lastName, partyID, watchListID, userRole
        FROM user
        WHERE userID = %s;
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query, (userID))
    retrieved_users = cursor.fetchall()

    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200

    return response
    
