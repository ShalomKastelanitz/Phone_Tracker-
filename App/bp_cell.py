from flask import Blueprint
from flask import  request, jsonify, current_app
import logging



from App.neo4j_service import longest_bluetooth_path, InserrCalls

blueprint_cell = Blueprint('/', __name__)


@blueprint_cell.route('/api/devices/bluetooth_connections', methods=['GET'])
def bluetooth_connections():
    return jsonify( longest_bluetooth_path()),200


@blueprint_cell.route('/api/devices/strong_signal', methods=['GET'])
def strong_signal():
    try:
        repo = InserrCalls(current_app.neo4j_driver)
        results = repo.devices_with_strong_signal()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blueprint_cell.route('/api/devices/<device_id>/connections/count', methods=['GET'])
def count_connections(device_id):
    try:
        repo = InserrCalls(current_app.neo4j_driver)
        count = repo.count_connections(device_id)
        return jsonify({'device_id': device_id, 'connection_count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blueprint_cell.route('/api/devices/direct_connection', methods=['POST'])
def direct_connection():
    data = request.get_json()
    try:
        repo = InserrCalls(current_app.neo4j_driver)
        is_connected = repo.direct_connection(data['from_id'], data['to_id'])
        return jsonify({'from_id': data['from_id'], 'to_id': data['to_id'], 'is_connected': is_connected}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blueprint_cell.route('/api/devices/<device_id>/latest_interaction', methods=['GET'])
def latest_interaction(device_id):
    try:
        repo = InserrCalls(current_app.neo4j_driver)
        interaction = repo.latest_interaction(device_id)
        return jsonify(interaction), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500








@blueprint_cell.route("/api/phone_tracker", methods=['POST'])
def insert_phone():
    data = request.get_json()
    if data['devices'][0]['id'] == data['devices'][1]['id']:
        return jsonify({'error': 'cannot can yourself'}), 400

    try:
        repo = InserrCalls(current_app.neo4j_driver)
        interaction_id = repo.create_call(data)
        return jsonify({
             'status': 'success',
            'transaction_id': interaction_id
            }), 201
    except Exception as e:
        print(f'Error in POST /api/phone_tracker: {str(e)}')
        logging.error(f'Error in POST /api/phone_tracker: {str(e)}')
        return jsonify({'error': 'internal server error'}), 500