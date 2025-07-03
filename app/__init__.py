from flask import Flask
from app.webhook.routes import webhook
from app.routes import ui
from dotenv import load_dotenv
from pathlib import Path
from .extensions import mongo

import os

# Creating our flask app
def create_app():
    path_to_env = Path('app/local.env')
    load_dotenv(dotenv_path=path_to_env)

    app = Flask(__name__)

    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(ui) # serves as the UI
    
    # Getting Mongo URI from environment file.
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    mongo.init_app(app)

    return app
