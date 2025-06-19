from ultralytics import YOLO
from flask import current_app as app
from app.api.GuitarTabs import Tab
def predict_frets():
    model = YOLO(app.config['MODEL_PATH'])
    model_results = model.predict(app.config['PROCESSED_FRAMES_FOLDER'])

    for i,result in enumerate(model_results):

        boxes = result.boxes
        frame = i 
        for box in boxes:
            # box in x, y, x, y
            x1,y1,x2,y2 = box.xyxy
            fret = box.cls
            position = [x1,y1,x2,y2]
            tab = Tab(fret, position,frame)
            print(tab)
            
            app.tracker.add_tab(tab)

    return {"success":True, "status": 200}

