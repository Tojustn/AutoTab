from flask import Flask, flash, request, url_for, redirect, session, send_from_directory
from flask import current_app as app
from werkzeug.utils import secure_filename
import json
from app.services.extract_frames import extract_frames
from app.services.is_chosen import is_chosen
from app.services.process_frames import preprocess_frames, get_string_from_frames, get_last_number
from app.model.predict import predict_frets
from app.services.user_session import get_session_id, init_session, get_user_paths, cleanup_user_data
from app.services.post_process_frames import render_tabs
import os
import shutil



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def register_routes(app):


    
    @app.route("/api/upload", methods = ["POST"])
    def upload_video():
        if(session.get("session_id") is None):
            init_session()
        user_paths = get_user_paths()
        # Remove directories if they exist, then recreate them
        for path in [user_paths["upload_path"], user_paths["file_path"], user_paths["processed_path"]]:
            if os.path.exists(path):
                shutil.rmtree(path)
        os.makedirs(user_paths["upload_path"], exist_ok=False)
        os.makedirs(user_paths["file_path"], exist_ok=False)
        os.makedirs(user_paths["processed_path"], exist_ok=False)

        if not request.files:
            return {"message": "No files received at all", "success": False} 

        if 'video' not in request.files:
            return {"message": "Missing 'video' in request.files", "status": 400}

        video = request.files['video']
        new_line_per_second = request.form.get("new_line")
        # Passed in as CSV
        frames_chosen = request.form.get("selected_frames") 
        frames_array = list(map(int, frames_chosen.split(","))) if frames_chosen else []
        print(frames_array)



        mode = "select" if frames_array is not None else "interval"  

        if not allowed_file(video.filename):
            return {"message":"File format not allowed", "status": 404}
        
        if(new_line_per_second):
            try:
                new_line_per_second = int(new_line_per_second) if new_line_per_second else 1
            except (ValueError, TypeError):
                new_line_per_second = 1
       

        filename = secure_filename(video.filename)
        upload_path = os.path.join(user_paths["upload_path"],filename)
        video.save(upload_path)
        extract_frames(upload_path, mode, new_line_per_second, frames_array)
        if not os.path.exists(upload_path):
            return {"message": "Could not extract frames", "status": 400}
        os.remove(upload_path)  
        return {"session_id": str(session.get("session_id")),"success":True, "status": 200}

    @app.route("/api/get_frame", methods = ["GET"])
    def get_frame():
        if(session.get("session_id") is None):
            init_session()
        user_paths = get_user_paths()
        # filter out the chosen_frames.json file
        frames = [frame for frame in os.listdir(user_paths["file_path"]) if frame.endswith('.jpg')]
        frames = sorted(frames, key = lambda x: get_last_number(x))

        frame= frames[0]
        # return file names
        return (f"/user_data/{session.get('session_id')}/static/frames/{frame}")

    @app.route('/user_data/<session_id>/static/frames/<filename>')
    def serve_frames(session_id, filename):
        return send_from_directory(os.path.join(os.getcwd(), f"user_data/{session_id}/static/frames"), filename)

    
    # Get the confirmed frames and send in as a list of numbers
    @app.route("/api/confirmed_frames", methods = ["POST"])
    def confirmed_frames():
        if(session.get("session_id") is None):
            init_session()
        
        # Work for both JSOn and Form Data
        if request.is_json:
            data = request.get_json()
            dimensions = data.get("dimensions")
            
        elif "dimensions" in request.form:
            # Parse json into a python dictionary
            dimensions = json.loads(request.form["dimensions"])

        for value in dimensions:
            dimensions[value] = int(dimensions[value])
        print(dimensions)
        
        preprocess_frames(dimensions)
        strings_capture_result = get_string_from_frames()
        if not strings_capture_result["success"]:
            return strings_capture_result
        predict_frets_result = predict_frets()
        if not predict_frets_result["success"]:
            return {"message": "Could not predict frets", "success": False, "status": 400}
        render_tabs_result = render_tabs()
        if not render_tabs_result["success"]:
            return {"message": "Could not render tabs", "success": False, "status": 400}
        return {"success":True, "status": 200, "result": render_tabs_result["result"]}
    
    # If a route fails, cleanup the user data so no errors
    @app.route("/api/cleanup", methods = ["DELETE"])
    def cleanup():
        cleanup_user_data();
