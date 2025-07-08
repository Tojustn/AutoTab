import cv2 as cv
import os
from flask import current_app
import json 
from app.services.user_session import get_user_paths

def extract_frames(filepath: str, new_line_per_second: int):
    user_paths = get_user_paths()
    if (new_line_per_second == -1):
        new_line_per_second = 1
    videoObj = cv.VideoCapture(filepath) 
    
    seconds = 1 # 1 second per frame
    count = 0
    frame_count = 0
    success = 1
    fps =  videoObj.get(cv.CAP_PROP_FPS)  
    chosen_frames = []

    # One frame per second will be saved
    frame_seconds_interval = fps*seconds

    while success:
        success, image = videoObj.read()
        if not success:
            break
            
        if frame_count % frame_seconds_interval == 0:
            uploadFiles = os.path.join(user_paths["file_path"], f"frame_{count}.jpg")
            cv.imwrite(uploadFiles, image)
            count += 1
            
            # Add frame to chosen frames if it meets the criteria
            if count % new_line_per_second == 0 and count > 0:
                chosen_frames.append(count)
            
        frame_count += 1
    
    # Store all chosen frames in a json file
    with open(os.path.join(user_paths["file_path"], 'chosen_frames.json'), 'w') as f:
        json.dump({"chosen_frames": chosen_frames, "total_frames": count}, f, indent=2)
    
    videoObj.release()
    return {"success": True, "total_frames": count, "chosen_frames": chosen_frames}