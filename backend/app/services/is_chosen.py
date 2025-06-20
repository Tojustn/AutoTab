import json
from app.services.process_frames import get_last_number
import os
from flask import current_app as app
def is_chosen(frame: str):
    with open(os.path.join(app.config['FRAMES_FOLDER'], 'chosen_frames.json'), 'r') as f:
        frame_data = json.load(f)
    if get_last_number(frame) in frame_data["chosen_frames"]:
        return True
    return False