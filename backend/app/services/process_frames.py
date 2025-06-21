import cv2 as cv
import os
from flask import current_app as app
import matplotlib.pyplot as plt
import numpy as np
import json
from app.services.user_session import get_user_paths
def get_last_number(frame: str) -> int:
    print(frame)
    return int(frame.split('_')[-1].split('.')[0])


def preprocess_frames(frames: list[int], dimensions: dict):
    # Check if chosen_frames.json exists first
    chosen_frames_path = os.path.join(get_user_paths()['file_path'], 'chosen_frames.json')
    if not os.path.exists(chosen_frames_path):
        print("chosen_frames.json not found")
        return
    
    # Open and read the file
    with open(chosen_frames_path, 'r') as f:
        frame_data = json.load(f)
    
    # Remove the file after reading
    os.remove(chosen_frames_path)
    
    # x left, y top, w width, h height
    x,y,w,h = dimensions.values()
    previous_frames = set()
    # Ensure processed frames directory exists
    os.makedirs(get_user_paths()['processed_path'], exist_ok=True)
    

    for frame in frames:
     
        if (frame not in previous_frames and f"frame_{frame}.jpg" in os.listdir(get_user_paths()['file_path'])):
            original_image = cv.imread(os.path.join(get_user_paths()['file_path'], f"frame_{frame}.jpg"))
            # Crop image to the dimensions
            cropped_image = original_image[y:y+h, x:x+w]
            cv.imwrite(os.path.join(get_user_paths()['processed_path'], f"frame_{frame}.jpg"), cropped_image)
            previous_frames.add(frame)
        else:
            continue
    
    # Delete all files in the FRAMES_FOLDER after processing
    for filename in os.listdir(get_user_paths()['file_path']):
        file_path = os.path.join(get_user_paths()['file_path'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_string_from_frames(): 
    processed_frames = sorted(os.listdir(get_user_paths()['processed_path']), key = lambda x: get_last_number(x))
    best_frame = None 
    for processed_frame in processed_frames:
        imgPath = os.path.join(get_user_paths()['processed_path'], processed_frame)
        grayscaled_image = cv.imread(imgPath,cv.IMREAD_GRAYSCALE)
        output = cv.cvtColor(grayscaled_image, cv.COLOR_GRAY2BGR) 
        # Edge Detection CannyEdge
        cannyEdge = cv.Canny(grayscaled_image, 100,150)
        # Ignore color
        height, width = grayscaled_image.shape[:2]

        #Using probablistic version so I can use the folloiwing:
        # minLineLength to avoid detecting numbers
        # minLineGap to merge close Lines on x file
        # Makes lines with x1,x2,y1,y2
        lines = cv.HoughLinesP(
            cannyEdge,
            rho=1,
            theta=np.pi / 180,
            threshold=80,
            minLineLength=width//1.5, # only long lines
            maxLineGap=40
        )

        #plt.imshow(cv.cvtColor(cannyEdge, cv.COLOR_BGR2RGB))
        #plt.show()

        # Since im already merging the x coords I now need to merge lines that are close on the x coordinates
        count = 0
        merged_lines = []

        previous_y = set() 

        if lines is not None:
            for i in range(len(lines)):
                x1, y1, x2, y2 = lines[i][0]
                middle_y = abs(y1+y2)/2
               # Filter: Only nearly horizontal lines
                if abs(y2 - y1) < 5:  # Y diff is very small meaning horizontal
                    if all(abs(middle_y - py) > height/10 for py in previous_y):
                        length = abs(x1 - x2)
                        merged_lines.append([0, middle_y, width, middle_y])
                        previous_y.add(middle_y)

        if merged_lines is not None:
            for i in range(len(merged_lines)):
                count+=1
                x1, y1, x2, y2 = merged_lines[i]

                cv.line(output, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                # Print image with lines
                

            plt.imshow(cv.cvtColor(output, cv.COLOR_BGR2RGB))
            plt.show()

        print(f"Merged lines: {len(merged_lines)}")
        if len(merged_lines) == 6:
            best_frame = processed_frame
            app.tracker.set_strings(merged_lines)
    print(f"Best frame: {best_frame}, Type: {type(best_frame)}")

    if best_frame is None:
        return {"message": "Could not extract strings", "success": False}
    return {"message": "Strings extracted", "success": True}
            
    