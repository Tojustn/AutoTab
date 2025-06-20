from ultralytics import YOLO
from flask import current_app as app
from app.api.GuitarTabs import Tab
def predict_frets():
    model = YOLO(app.config['MODEL_PATH'])
    model_results = model.predict(app.config['PROCESSED_FRAMES_FOLDER'])
    if model_results[0].boxes.cls is None:
        return {"success":False, "status": 400, "message": "No frets detected"}

    for i,result in enumerate(model_results):

        boxes = result.boxes
        frame = i + 1
        for box in boxes:
            
            # box in x, y, x, y
            
            x1,y1,x2,y2 = box.xyxy[0]
            fretx = int(box.cls[0])
            # Convert from class indices to names
            fretName = model.names[fretx]
            position = [x1,y1,x2,y2]
            print(box.xyxy)
            print(fretName)
            print(position)
            tab = Tab(fretName, position,frame)
            print(tab)
            
            app.tracker.add_tab(tab)

    return {"success":True, "status": 200}

