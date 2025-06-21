import os 
from flask import current_app as app
    
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
model_path = os.path.join(base_dir, 'app', 'model', 'GuitarTabPredictionModel.pt')

class Config:
    ALLOWED_EXTENSIONS = {"mp4"}

    MODEL_PATH = model_path
    TESTING = False


# Config for testing 
class TestConfig(Config):
    TESTING = True
    test_base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
