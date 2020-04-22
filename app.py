import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from casting.casting import casting
from errorhandler.errorhandler import error


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(casting)
    app.register_blueprint(error)
    CORS(app)
    setup_db(app)

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)
