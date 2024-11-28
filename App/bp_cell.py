from flask import Blueprint, request, jsonify, current_app
import json
import logging
from neo4j_service import InsightsRepository

insights_bp = Blueprint('insights_bp', __name__)

@insights_bp.route("/api/insights/bluetooth_connections", methods=['GET'])
def fetch_bluetooth_connections():
    try:
        repo = InsightsRepository(current_app.neo4j_driver)
        path_length = repo.get_bluetooth_connections()

        return jsonify({"path_length": path_length}), 200
    except Exception as e:
        print(f'Error in GET /api/insights/bluetooth_connections: {str(e)}')
        logging.error(f'Error in GET /api/insights/bluetooth_connections: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500

@insights_bp.route("/api/insights/signal_strength", methods=['GET'])
def fetch_signal_strength():
    try:
        repo = InsightsRepository(current_app.neo4j_driver)
        signals = repo.get_signal_strength()

        return jsonify(signals), 200
    except Exception as e:
        print(f'Error in GET /api/insights/signal_strength: {str(e)}')
        logging.error(f'Error in GET /api/insights/signal_strength: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500


@insights_bp.route("/api/insights/connected_count/<device_id>", methods=['GET'])
def fetch_connected_count(device_id):
    try:
        repo = InsightsRepository(current_app.neo4j_driver)
        connected_count = repo.get_connected_count(device_id)

        return jsonify({"connected_count": connected_count}), 200
    except Exception as e:
        print(f'Error in GET /api/insights/connected_count: {str(e)}')
        logging.error(f'Error in GET /api/insights/connected_count: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500


@insights_bp.route("/api/insights/connection_status/<device_id1>/<device_id2>", methods=['GET'])
def fetch_connection_status(device_id1, device_id2):
    try:
        repo = InsightsRepository(current_app.neo4j_driver)
        is_connected = repo.check_connection_status(device_id1, device_id2)

        return jsonify(is_connected), 200
    except Exception as e:
        print(f'Error in GET /api/insights/connection_status: {str(e)}')
        logging.error(f'Error in GET /api/insights/connection_status: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500

@insights_bp.route("/api/insights/last_interaction/<device_id>", methods=['GET'])
def fetch_last_interaction(device_id):
    try:
        repo = InsightsRepository(current_app.neo4j_driver)
        last_interaction = repo.get_last_interaction(device_id)

        return jsonify(last_interaction), 200
    except Exception as e:
        print(f'Error in GET /api/insights/last_interaction: {str(e)}')
        logging.error(f'Error in GET /api/insights/last_interaction: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500
