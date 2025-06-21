from flask import Flask, flash, request, url_for, redirect, session
from flask import current_app as app
from werkzeug.utils import secure_filename
from app.services.extract_frames import extract_frames
from app.services.is_chosen import is_chosen
from app.services.process_frames import preprocess_frames, get_string_from_frames, get_last_number
from app.model.predict import predict_frets
from app.services.user_session import get_session_id, init_session, get_user_paths
import os


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def register_routes(app):


    
    @app.route("/api/upload", methods = ["POST"])
    def upload_video():
        if(session.get("session_id") is None):
            init_session()
        user_paths = get_user_paths()
        os.makedirs(user_paths["upload_path"], exist_ok=True)
        os.makedirs(user_paths["file_path"], exist_ok=True)
        os.makedirs(user_paths["processed_path"], exist_ok=True)

        if 'video' not in request.files:
            return {"message": "Missing 'video' in request.files", "status": 400}

        video = request.files['video']
        new_line_per_second = request.form.get("new_line")
        print(f"Received new_line from form: {new_line_per_second}")
        
        # Handle the new_line parameter more robustly
        try:
            new_line_per_second = int(new_line_per_second) if new_line_per_second else 1
        except (ValueError, TypeError):
            new_line_per_second = 1
        
        print(f"Using new_line_per_second: {new_line_per_second}")
        
        if not allowed_file(video.filename):
            return {"message":"File format not allowed", "status": 404}

        
        filename = secure_filename(video.filename)
        video.save(os.path.join(user_paths["upload_path"], filename))
        extract_frames(os.path.join(user_paths["upload_path"], filename), new_line_per_second)
        if not os.path.exists(os.path.join(user_paths["upload_path"], filename)):
            return {"message": "Could not extract frames", "status": 400}
        os.remove(os.path.join(user_paths["upload_path"], filename))  
        return {"success":True, "status": 200}

    @app.route("/api/get_frames", methods = ["GET"])
    def get_frames():
        if(session.get("session_id") is None):
            init_session()
        user_paths = get_user_paths()
        # filter out the chosen_frames.json file
        frames = [frame for frame in os.listdir(user_paths["file_path"]) if frame.endswith('.jpg')]
        frames = sorted(frames, key = lambda x: get_last_number(x))

        # return file names
        return [(f"/user_data/{session.get('session_id')}/static/frames/{frame}", is_chosen(frame)) for frame in frames]
    
    # Get the confirmed frames and send in as a list of numbers
    @app.route("/api/confirmed_frames", methods = ["POST"])
    def confirmed_frames():
        if(session.get("session_id") is None):
            init_session()
        frames = request.json.get("frames")
        # Crop the frames to the dimensions before resizing
        dimensions = request.json.get("dimensions")
        #print(frames)
       #print(type(frames))
        print(dimensions)
        preprocess_frames(frames, dimensions)
        strings_capture_result = get_string_from_frames()
        if not strings_capture_result["success"]:
            return strings_capture_result
        predict_frets_result = predict_frets()
        if not predict_frets_result["success"]:
            return {"message": "Could not predict frets", "success": False, "status": 400}
        return {"success":True, "status": 200}
