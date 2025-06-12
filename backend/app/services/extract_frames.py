import cv2 as cv

def extract_frames(filepath: str):
    videoObj = cv.VideoCapture(filepath)
    
    count = 0 
    success = 1
    while success:
        success, image = videoObj.read()
        uploadFiles = os.path.join(app.config['UPLOAD_FOLDER'],f"frame_{count}.jpg")
        cv.imwrite(uploadFiles, image)
        count+=1
