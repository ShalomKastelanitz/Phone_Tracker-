from flask import Blueprint, request, jsonify, current_app
import json
import logging
from neo4j_service_create import CallsHandlerRepository

calls_bp = Blueprint('calls_bp', __name__)

@calls_bp.route("/api/phone_tracker", methods=['POST'])
def add_call_log():
    data = request.get_json()
    if data['devices'][0]['id'] == data['devices'][1]['id']:
        return jsonify({'error': 'cannot call yourself'}), 400

    try:
        repo = CallsHandlerRepository(current_app.neo4j_driver)
        call_id = repo.save_call(data)

        return jsonify({
            'status': 'success',
            'call_id': call_id
        }), 201
    except Exception as e:
        print(f'Error in POST /api/call_logs: {str(e)}')
        logging.error(f'Error in POST /api/call_logs: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500
