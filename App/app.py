from flask import Flask
import logging

from App.bp_cell import blueprint_cell
from init_db import init_neo4j


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['LOGGING_LEVEL'] = logging.DEBUG



with app.app_context():
    app.neo4j_driver = init_neo4j()


app.register_blueprint(blueprint_cell)

if __name__ == "__main__":
    app.run(debug=True)