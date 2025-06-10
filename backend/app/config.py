import os 

    
base_dir = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(base_dir, 'data', 'raw_videos')

class Config:
    ALLOWED_EXTENSIONS = {"mp4"}
    UPLOAD_FOLDER = upload_path