import json
from app.services.process_frames import get_last_number
import os
from flask import current_app as app
from app.services.user_session import get_user_paths
def is_chosen(frame: str):
    user_paths = get_user_paths()
    with open(os.path.join(user_paths["file_path"], 'chosen_frames.json'), 'r') as f:
        frame_data = json.load(f)
    if get_last_number(frame) in frame_data["chosen_frames"]:
        return True
    return False