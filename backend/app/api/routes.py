from flask import Flask, flash, request, url_for, redirect
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def register_routes(app):
    @app.route("/api/upload", methods = ["POST"])
    def upload_video():
        allowed_file_formats = ['mp4']
        video = request.files['video']

        bpm = request.form.get['bpm']
        if not allowed_file(video.filename):
            return {"message":"File format not allowed", "status": 404}
        
        filename = secure_filename(file.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {
    "message": "Upload successful",
    "filename": filename
}