from flask import Blueprint, jsonify
from flask import current_app
from backend.ml_models.logreg import predict

logreg_bp = Blueprint('customer', __name__)

@logreg_bp.route('/prediction/<party>/<procedure_type>', methods=['GET'])
def get_prediction(party, procedure_type):
    try:
        current_app.logger.info(f"Received prediction request for party={party}, procedure_type={procedure_type}")

        # Call model prediction function
        result = predict(party, procedure_type)

        # Return result
        
        return jsonify({'prediction': round(result, 2)})

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        current_app.logger.error(f"Prediction error: {e}\n{error_msg}")
        return jsonify({'error': 'Prediction failed'}), 500

