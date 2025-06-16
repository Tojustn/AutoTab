import os 
from flask import current_app as app
    
base_dir = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(base_dir, 'data', 'raw_videos')

frames_path = os.path.join(base_dir, 'static','frames')

processed_frames_path = os.path.join(base_dir, 'data', 'processed_frames')
class Config:
    ALLOWED_EXTENSIONS = {"mp4"}
    UPLOAD_FOLDER = upload_path
    FRAMES_FOLDER = frames_path
    PROCESSED_FRAMES_FOLDER = processed_frames_path