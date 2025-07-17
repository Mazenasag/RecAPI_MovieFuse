import pytest
from app import app  # ✅ correct: no `.py`, just the module name

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_recommendations_found(client):
    response = client.post('/', data={'title': 'The Matrix'})  # Replace with a valid movie title
    assert response.status_code == 200
    assert b'Recommendations for' in response.data

def test_title_not_found(client):
    response = client.post('/', data={'title': 'SomeFakeMovieThatDoesNotExist'})
    assert response.status_code == 200
    assert b'Title not found in dataset.' in response.data

def test_get_request(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Enter movie title...' in response.data
