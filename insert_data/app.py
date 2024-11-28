from flask import Flask
from flask import  request, jsonify, current_app
import logging
from neo4j_service import InserrCalls
from init_db import init_neo4j


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['LOGGING_LEVEL'] = logging.DEBUG



with app.app_context():
    app.neo4j_driver = init_neo4j()

@app.route("/api/phone_tracker", methods=['POST'])
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

if __name__ == "__main__":
    app.run(debug=True)