from flask import Flask
from flask_cors import CORS
from app.api.routes.process_routes import register_process_routes 
from app.api.routes.youtube_routes import register_youtube_routes
def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Temporary folder for saving video files
    app.config["UPLOAD_FOLDER"] = "temp/"

    register_youtube_routes(app)
    register_process_routes(app)

    return app