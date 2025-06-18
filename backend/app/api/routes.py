from flask import Flask, flash, request, url_for, redirect
from flask import current_app as app
from werkzeug.utils import secure_filename
from app.services.extract_frames import extract_frames
from app.services.process_frames import preprocess_frames, get_string_from_frames
import os
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Fetch the last number of the frames
def get_last_number(frame: str) -> int:
    print(frame)
    return int(frame.split('_')[-1].split('.')[0])

def register_routes(app):
    @app.route("/api/upload", methods = ["POST"])
    def upload_video():
        if 'video' not in request.files:
            return {"message": "Missing 'video' in request.files", "status": 400}

        video = request.files['video']

        if not allowed_file(video.filename):
            return {"message":"File format not allowed", "status": 404}

        
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        extract_frames(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
        return {"success":True, "status": 200}

    @app.route("/api/get_frames", methods = ["GET"])
    def get_frames():
        frames = sorted(os.listdir(app.config['FRAMES_FOLDER']), key = lambda x: get_last_number(x))
        # return file names
        return [f"/static/frames/{frame}" for frame in frames]
    
    # Get the confirmed frames and send in as a list of numbers
    @app.route("/api/confirmed_frames", methods = ["POST"])
    def confirmed_frames():
        frames = request.json.get("frames")
        dimensions = request.json.get("dimensions")
        #print(frames)
       #print(type(frames))
        print(dimensions)
        preprocess_frames(frames, dimensions)
        strings_capture_result = get_string_from_frames()
        if not strings_capture_result["success"]:
            return strings_capture_result
        return {"success":True, "status": 200}
