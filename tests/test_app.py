import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_pdf(client):
    with open('test.pdf', 'rb') as f:
        response = client.post('/upload', data={'file': f})
        assert response.status_code == 200

def test_ask_question(client):
    context = "Some extracted text from PDF."
    response = client.post('/ask', json={'question': 'What is this about?', 'context': context})
    assert response.status_code == 200
