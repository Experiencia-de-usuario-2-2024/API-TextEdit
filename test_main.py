from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Prueba unitaria: Verifica que la raíz de la API responde correctamente
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "documentation_url" in response.json()

# Prueba unitaria: Verifica que el análisis de sentimiento funciona correctamente con texto válido
def test_analyze_sentiment():
    response = client.post("/sentiment", json={"text": "I love this!"})
    assert response.status_code == 200
    json_response = response.json()
    assert "sentiment" in json_response
    assert "score" in json_response

# Prueba unitaria: Verifica que el análisis de emociones funciona correctamente con texto válido
def test_analyze_emotions():
    response = client.post("/emotions", json={"texto": "Estoy muy feliz"})
    assert response.status_code == 200
    json_response = response.json()
    assert "emoción_principal" in json_response

# Prueba unitaria: Verifica que la clasificación de texto funciona correctamente con texto válido
def test_classify_text():
    response = client.post("/classify", json={"texto": "Estoy de acuerdo con esto"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response
    assert "duda" in json_response
    assert "acuerdo" in json_response
    assert "desacuerdo" in json_response

# Prueba unitaria: Verifica que el análisis de desacuerdos funciona correctamente con texto válido
def test_analyze_disagreement():
    response = client.post("/desacuerdos", json={"texto": "Creo que esto es bueno: No, esto es malo"})
    assert response.status_code == 200
    json_response = response.json()
    assert "postura1" in json_response
    assert "postura2" in json_response

# Prueba unitaria: Verifica que la creación de compromisos funciona correctamente con texto válido
def test_create_commitment():
    response = client.post("/compromiso", json={"texto": "Juan va a hacer cambio en la base de datos mañana en la oficina"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response

# Pruebas unitarias: Verifica que los endpoints manejan correctamente el texto vacío
def test_empty_text_sentiment():
    response = client.post("/sentiment", json={"text": ""})
    assert response.status_code == 400

def test_empty_text_emotions():
    response = client.post("/emotions", json={"texto": ""})
    assert response.status_code == 400

def test_empty_text_classify():
    response = client.post("/classify", json={"texto": ""})
    assert response.status_code == 400

def test_empty_text_disagreement():
    response = client.post("/desacuerdos", json={"texto": ""})
    assert response.status_code == 400

def test_empty_text_commitment():
    response = client.post("/compromiso", json={"texto": ""})
    assert response.status_code == 400

# Pruebas unitarias: Verifica que los endpoints manejan correctamente peticiones con datos inexistentes
def test_nonexistent_text_sentiment():
    response = client.post("/sentiment", json={})
    assert response.status_code == 422

def test_nonexistent_text_emotions():
    response = client.post("/emotions", json={})
    assert response.status_code == 422

def test_nonexistent_text_classify():
    response = client.post("/classify", json={})
    assert response.status_code == 422

def test_nonexistent_text_disagreement():
    response = client.post("/desacuerdos", json={})
    assert response.status_code == 422

def test_nonexistent_text_commitment():
    response = client.post("/compromiso", json={})
    assert response.status_code == 422

# Prueba de integración: Simula el envío de múltiples solicitudes simultáneas para el análisis de sentimientos
def test_multiple_simultaneous_requests():
    responses = []
    for _ in range(10):
        response = client.post("/sentiment", json={"text": "This is a test"})
        responses.append(response)
    
    for response in responses:
        assert response.status_code == 200

# Pruebas unitarias: Verifica que los endpoints manejan correctamente textos largos
def test_long_text_sentiment():
    long_text = "Estoy muy feliz " * 50  # Ajusta según tus necesidades
    response = client.post("/sentiment", json={"text": long_text})
    assert response.status_code == 200
    json_response = response.json()
    assert "sentiment" in json_response
    assert "score" in json_response

def test_long_text_emotions():
    long_text = "Estoy muy feliz. " * 50  # Ajusta según tus necesidades
    response = client.post("/emotions", json={"texto": long_text})
    assert response.status_code == 200
    json_response = response.json()
    assert "emoción_principal" in json_response

# Prueba unitaria: Verifica que el análisis de emociones maneja correctamente texto en otro idioma
def test_non_english_text_emotions():
    response = client.post("/emotions", json={"texto": "Je suis très heureux"})
    assert response.status_code == 200
    json_response = response.json()
    assert "emoción_principal" in json_response

# Prueba unitaria: Verifica que la clasificación de texto maneja correctamente caracteres especiales
def test_special_characters_classify():
    response = client.post("/classify", json={"texto": "@#$%^&*()"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response
    assert "duda" in json_response
    assert "acuerdo" in json_response
    assert "desacuerdo" in json_response

# Prueba unitaria: Verifica que los endpoints manejan correctamente múltiples peticiones con texto vacío
def test_empty_text_responses():
    endpoints = [
        ("/sentiment", {"text": ""}),
        ("/emotions", {"texto": ""}),
        ("/classify", {"texto": ""}),
        ("/desacuerdos", {"texto": ""}),
        ("/compromiso", {"texto": ""})
    ]
    
    for endpoint, payload in endpoints:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de análisis de sentimientos maneja correctamente textos con solo espacios
def test_spaces_text_sentiment():
    response = client.post("/sentiment", json={"text": " "})
    assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de análisis de emociones maneja correctamente textos con solo espacios
def test_spaces_text_emotions():
    response = client.post("/emotions", json={"texto": " "})
    assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de clasificación maneja correctamente textos con solo espacios
def test_spaces_text_classify():
    response = client.post("/classify", json={"texto": " "})
    assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de desacuerdos maneja correctamente textos con solo espacios
def test_spaces_text_disagreement():
    response = client.post("/desacuerdos", json={"texto": " "})
    assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de compromisos maneja correctamente textos con solo espacios
def test_spaces_text_commitment():
    response = client.post("/compromiso", json={"texto": " "})
    assert response.status_code == 400

# Prueba unitaria: Verifica que el endpoint de análisis de sentimientos maneja correctamente entradas con números
def test_numbers_text_sentiment():
    response = client.post("/sentiment", json={"text": "12345"})
    assert response.status_code == 200
    json_response = response.json()
    assert "sentiment" in json_response
    assert "score" in json_response

# Prueba unitaria: Verifica que el endpoint de análisis de emociones maneja correctamente entradas con números
def test_numbers_text_emotions():
    response = client.post("/emotions", json={"texto": "12345"})
    assert response.status_code == 200
    json_response = response.json()
    assert "emoción_principal" in json_response

# Prueba unitaria: Verifica que el endpoint de clasificación maneja correctamente entradas con números
def test_numbers_text_classify():
    response = client.post("/classify", json={"texto": "12345"})
    assert response.status_code == 200
    json_response = response.json()
    assert "compromiso" in json_response
    assert "duda" in json_response
    assert "acuerdo" in json_response
    assert "desacuerdo" in json_response

# Prueba unitaria: Verifica que el endpoint de desacuerdos maneja correctamente entradas con números
def test_numbers_text_disagreement():
    response = client.post("/desacuerdos", json={"texto": "12345"})
    assert response.status_code == 200
    json_response = response.json()
    assert "postura1" in json_response
    assert "postura2" in json_response

# Prueba de rendimiento: Verifica que el tiempo de respuesta sea aceptable
def test_performance():
    import time
    start_time = time.time()
    response = client.post("/sentiment", json={"text": "This is a performance test"})
    end_time = time.time()
    assert response.status_code == 200
    assert (end_time - start_time) < 1  # La respuesta debe ser en menos de 1 segundo
