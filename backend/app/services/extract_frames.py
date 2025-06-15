import cv2 as cv
import os
from flask import current_app

def extract_frames(filepath: str):
    videoObj = cv.VideoCapture(filepath) 
    
    seconds = 1 # 1 second per frame
    count = 0
    frame_count = 0
    success = 1
    fps =  videoObj.get(cv.CAP_PROP_FPS)  

    frame_interval = fps*seconds
    while success:
        success, image = videoObj.read()
        if not success:
            return {"success": False, "status": 404}

            break
            
        if frame_count % frame_interval == 0:
            uploadFiles = os.path.join(current_app.config['FRAMES_FOLDER'], f"frame_{count}.jpg")
            cv.imwrite(uploadFiles, image)
            count += 1
            
        frame_count += 1
        
    return