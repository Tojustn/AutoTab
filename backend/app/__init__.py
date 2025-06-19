from flask import Flask
from flask_cors import CORS
from app.api.routes import register_routes
from .config import Config, TestConfig
from .api.GuitarTabs import GuitarTabs

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Temporary folder for saving video files
    app.config.from_object(TestConfig)

    register_routes(app)

    tracker = GuitarTabs()
    app.tracker = tracker


    return app