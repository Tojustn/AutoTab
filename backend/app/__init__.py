from flask import Flask, session
from flask_cors import CORS
from app.api.routes import register_routes
from .config import Config, TestConfig
from .api.GuitarTabs import GuitarTabs
from dotenv import load_dotenv
import uuid
import os


def create_app():
    # Load environment variables from .env file
    # Specify the path explicitly to ensure it's found
    load_dotenv()
    
    os.getenv("SECRET_KEY")
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # Temporary folder for saving video files
    app.config.from_object(Config)

    register_routes(app)

    tracker = GuitarTabs()
    app.tracker = tracker

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_ID'] = False

    return app


