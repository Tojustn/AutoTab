import pytest
from app import create_app
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app 

    # teardown 

# Pytest looks for app fixture and passes it to the client function
@pytest.fixture()
def client(app):
    return app.test_client()