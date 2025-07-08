from main import app
from app.model.predict import predict_frets
from app.services.user_session import get_session_id
import uuid

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