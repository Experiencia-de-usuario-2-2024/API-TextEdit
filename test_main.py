from fastapi.testclient import TestClient
from main import app  # Asegúrate de que 'main' es el nombre de tu archivo principal

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "documentation_url" in response.json()

def test_analyze_sentiment():
    response = client.post("/sentiment", json={"text": "I love this!"})
    assert response.status_code == 200
    json_response = response.json()
    assert "sentiment" in json_response
    assert "score" in json_response

def test_analyze_emotions():
    response = client.post("/emotions", json={"texto": "Estoy muy feliz"})
    assert response.status_code == 200
    json_response = response.json()
    assert "emoción_principal" in json_response

def test_classify_text():
    response = client.post("/classify", json={"texto": "Estoy de acuerdo con esto"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response
    assert "duda" in json_response
    assert "acuerdo" in json_response
    assert "desacuerdo" in json_response

def test_analyze_disagreement():
    response = client.post("/desacuerdos", json={"texto": "Creo que esto es bueno: No, esto es malo"})
    assert response.status_code == 200
    json_response = response.json()
    assert "postura1" in json_response
    assert "postura2" in json_response

def test_create_commitment():
    response = client.post("/compromiso", json={"texto": "Juan va a hacer cambio en la base de datos mañana en la oficina"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response

