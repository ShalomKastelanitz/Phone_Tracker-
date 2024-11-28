from flask import Flask
import logging

from App.bl_create import calls_bp
from App.bp_cell import insights_bp
from init_db import init_neo4j


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['LOGGING_LEVEL'] = logging.DEBUG

app.register_blueprint(insights_bp, url_prefix='/api/insights')
app.register_blueprint(calls_bp)

with app.app_context():
    app.neo4j_driver = init_neo4j()



if __name__ == "__main__":
    app.run(debug=True)