from flask import Blueprint, jsonify, request

# Create a blueprint for recommendation routes
recommendation = Blueprint('recommendation', __name__)

@recommendation.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Recommendation route active"}), 200

@recommendation.route('/', methods=['GET'])
def recommend_home():
    return jsonify({"message": "Welcome to the Recommendation API!"}), 200

@recommendation.route("/generate", methods=["POST"])
def generate_recommendation():
    data = request.get_json()


    # Example recommendation result
    recommendation_result = {
        "recommendations": [
            {"mep_id": 9689, "score": 0.92},
            {"mep_id": 4462, "score": 0.87},
        ]
    }

    return jsonify(recommendation_result), 200