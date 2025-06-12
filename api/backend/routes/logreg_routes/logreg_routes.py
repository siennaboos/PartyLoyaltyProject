from flask import Blueprint, jsonify, request
from flask import current_app
from backend.ml_models.logreg import predict

logreg_bp = Blueprint('logreg', __name__)


@logreg_bp.route('/prediction', methods=['GET'])
def get_prediction():
    try:
        data = request.get_json(force=True)
        # log inputs
        current_app.logger.info(f"Received prediction request for parties={data['Parties']}, procedure_type={data['Procedures']}")

        # call model prediction function
        result = predict(data['Parties'], data['Procedures'])

        # return the result as json
        return jsonify({'prediction': round(result, 2)})

    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500