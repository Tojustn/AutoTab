import cv2 as cv
import os
from flask import current_app as app
import matplotlib.pyplot as plt
import numpy as np

def get_last_number(frame: str) -> int:
    return int(frame.split('_')[-1].split('.')[0])


def preprocess_frames(frames: list[int]):
    previous_frames = set()
    # Ensure processed frames directory exists
    os.makedirs(app.config['PROCESSED_FRAMES_FOLDER'], exist_ok=True)
    
    for frame in frames:
        if frame not in previous_frames and f"frame_{frame}.jpg" in os.listdir(app.config['FRAMES_FOLDER']):
            image = cv.imread(os.path.join(app.config['FRAMES_FOLDER'], f"frame_{frame}.jpg"))
            resized_image = cv.resize(image, (640,640))
            grayscaled_image = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)
            # No blur since image is already basic enough
            cv.imwrite(os.path.join(app.config['PROCESSED_FRAMES_FOLDER'], f"frame_{frame}.jpg"), grayscaled_image)
            previous_frames.add(frame)
        else:
            continue
    
    # Delete all files in the FRAMES_FOLDER after processing
    for filename in os.listdir(app.config['FRAMES_FOLDER']):
        file_path = os.path.join(app.config['FRAMES_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_string_from_frames(): 
    processed_frames = sorted(os.listdir(app.config['PROCESSED_FRAMES_FOLDER']), key = lambda x: get_last_number(x))
    best_frame = None
    for processed_frame in processed_frames:
        imgPath = os.path.join(app.config['PROCESSED_FRAMES_FOLDER'], processed_frame)
        grayscaled_image = cv.imread(imgPath,cv.IMREAD_GRAYSCALE)
        cropped_image = grayscaled_image[100:540, 0:640]
        output = cv.cvtColor(cropped_image, cv.COLOR_GRAY2BGR) 
        # Edge Detection CannyEdge
        cannyEdge = cv.Canny(cropped_image, 100,150)
        height, width = cropped_image.shape

        #Using probablistic version so I can use the folloiwing:
        # minLineLength to avoid detecting numbers
        # minLineGap to merge close Lines on x file
        # Makes lines with x1,x2,y1,y2
        lines = cv.HoughLinesP(
            cannyEdge,
            rho=1,
            theta=np.pi / 180,
            threshold=80,
            minLineLength=img.shape[1]//5, # only long lines
            maxLineGap=40
        )

        #plt.imshow(cv.cvtColor(cannyEdge, cv.COLOR_BGR2RGB))
        #plt.show()

        # Since im already merging the x coords I now need to merge lines that are close on the x coordinates
        count = 0
        merged_lines = set()
        previous_y = set() 

        if lines is not None:
            for i in range(len(lines)):
                x1, y1, x2, y2 = lines[i][0]
                middle_y = abs(y1+y2)/2
               # Filter: Only nearly horizontal lines
                if abs(y2 - y1) < 5:  # Y diff is very small meaning horizontal
                    if all(abs(middle_y - py) > 10 for py in previous_y):
                        length = abs(x1 - x2)
                        merged_lines.add([0, middle_y, width, middle_y])
                        previous_y.add(middle_y)

        if merged_lines is not None:
            for i in range(len(merged_lines)):
                count+=1
                x1, y1, x2, y2 = merged_lines[i]

                cv.line(output, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

        if len(merged_lines) > 6:
            best_frame = processed_frame
    if best_frame is None:
        return {"message": "Could not extract strings", "success": False}
    else:
        app.tracker.set_strings(merged_lines)
        return {"message": "Strings extracted", "success": True}
            
    

def label_frames():
    pass