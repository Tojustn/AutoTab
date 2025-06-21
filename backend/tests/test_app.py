import io
from main import app
from app.model.predict import predict_frets
from app.services.user_session import init_session, get_session_id
import os

import uuid

def test_upload_video(client):

    # In memory fake video
    video = (io.BytesIO(b"fake mp4 content"), "video.mp4")
    new_line_per_second = 1
    data = {
        "video": video,
        "new_line": new_line_per_second
    }

    response = client.post(
        "/api/upload",
        data=data,
        content_type="multipart/form-data"
    )
    assert response.json == {"success":True, "status": 200}



def test_get_frames(client):
    response = client.get("/api/get_frames")

    assert response.status_code == 200

    frame_urls = response.json

    assert isinstance(frame_urls, list)
    assert all(url.startswith("/static/frames/") for url in frame_urls)

def test_confirmed_frames(client):

    payload = {
    "frames": [5,6,7,8,9],
    "dimensions": {"x" : 50, "y" : 0 , "width" : 100, "height" : 640}
}

    response = client.post("/api/confirmed_frames", json=payload, content_type="application/json")
    assert response.json  == {"success":True, "status": 200} or response.json == {"message": "Could not extract strings", "success": False}



def test_predict_frets(client):
    with app.app_context():
        # Need app context since not in a request
        response = predict_frets()
        assert response == {"success":True, "status": 200}



def test_get_session_id(client):
    with app.app_context():
        # Test that get_session_id returns a UUID
        session_id = get_session_id()
        assert type(session_id) == uuid.UUID
        
        # Test that it generates different UUIDs
        session_id2 = get_session_id()
        assert session_id != session_id2


