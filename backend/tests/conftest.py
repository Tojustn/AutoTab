import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

@pytest.fixture()
def app():
    app = create_app()


    yield app 

    # teardown 
    

# Pytest looks for app fixture and passes it to the client function
@pytest.fixture()
def client(app):
    return app.test_client()