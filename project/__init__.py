# project/__init__.py

import os
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# Instantiate database 
db = SQLAlchemy()


def create_app():
    """Flask Application Factory"""

    # Instantiate flask app
    app = Flask(__name__)

    # Get configuration from environment/container, then apply config to app
    # 'docker-compose.yml' will set the container's APP_SETTINGS variable
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Connect SQLAlchemy extension
    db.init_app(app)

    # Register blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)


    return app
