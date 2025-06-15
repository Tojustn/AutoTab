import cv2 as cv
import os
import current_app as app
def process_frames(frames: list[int]):
    for frame in frames:
        if os.path.join(app.config['FRAMES_FOLDER'], f"frame_{frame}.jpg") in os.listdir(app.config['FRAMES_FOLDER']):
            image = cv.imread(os.path.join(app.config['FRAMES_FOLDER'], f"frame_{frame}.jpg"))
            resized_image = cv.resize(image, (640,640))
            grayscaled_image = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)
            # No blur since image is already basic enough
            os.imwrite(os.path.join(app.config['PROCESSED_FRAMES_FOLDER'], f"frame_{frame}.jpg"), grayscaled_image)
        else:
            continue
    
    # Delete all files in the FRAMES_FOLDER after processing
    for filename in os.listdir(app.config['FRAMES_FOLDER']):
        file_path = os.path.join(app.config['FRAMES_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
