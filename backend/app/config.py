import os 

class Config:
    ALLOWED_EXTENSIONS = {"mp4"}
    UPLOAD_FOLDER = os.path.join("data", "raw_videos")