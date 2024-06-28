from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from fastapi.middleware.cors import CORSMiddleware

from transformers import pipeline
import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from fastapi.responses import JSONResponse

import re

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(title="TextEdit API", description="API para análisis de sentimientos y emociones en texto.")

# Cargar el pipeline de transformers para análisis de sentimientos
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
# Carga del modelo para análisis de emociones
classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", top_k=None)

# Define el diccionario de traducción de emociones
emotion_translation = {
    'sadness': 'tristeza',
    'joy': 'alegría',
    'love': 'amor',
    'anger': 'enfado',
    'fear': 'miedo',
    'surprise': 'sorpresa'
}

# Configuración del cliente de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Configuración de CORS
origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
    "https://localhost",
    "https://localhost:3001",
    "https://localhost:3000",
    "https://localhost:8000",
    
    # Añade aquí otros orígenes que necesites permitir
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos para la entrada de datos
class SentimentRequest(BaseModel):
    text: str

class EmotionRequest(BaseModel):
    texto: str

class ClassificationRequest(BaseModel):
    texto: str

class ElementInfoRequest(BaseModel):
    texto: str


@app.get("/", summary="Saludo y Enlace a la Documentación", description="Proporciona un enlace directo a la documentación de la API para obtener más información sobre los endpoints disponibles y su uso.")
def read_root(request: Request):
    base_url = str(request.base_url)
    documentation_url = f"{base_url}docs"
    return JSONResponse(
        content={"message": "Para ver la documentación de la API, visita el siguiente enlace:", "documentation_url": documentation_url},
        status_code=200,
    )

@app.post("/sentiment", summary="Analizar Sentimiento", description="Analiza el sentimiento del texto proporcionado.")
async def analyze_sentiment(request: SentimentRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Uso del modelo para predecir el sentimiento de manera asíncrona
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: sentiment_pipeline(text))
    sentiment = result[0]['label']
    score = result[0]['score']

    # Mapear las etiquetas del modelo a términos más claros
    if sentiment == "LABEL_0":
        sentiment = "NEGATIVO"
    elif sentiment == "LABEL_1":
        sentiment = "POSITIVO"

    return {"sentiment": sentiment, "score": score}

# Define el endpoint para analizar emociones
@app.post("/emotions", summary="Analizar Emociones", description="Analiza las emociones en un texto en español.")
async def analyze_emotions(request: EmotionRequest):
    text = request.texto.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Traduce el texto de español a inglés
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)

    # Realiza la predicción de emociones en el texto traducido
    prediction = classifier(translated_text)
    
    # Simplifica la estructura de la respuesta
    simplified_prediction = prediction[0]  # Elimina el primer nivel de la lista

    # Traduce las etiquetas de emoción al español
    translated_prediction = [{**emotion, 'label': emotion_translation[emotion['label']]} for emotion in simplified_prediction]
    
    # Encuentra la emoción con el mayor puntaje
    max_emotion = max(translated_prediction, key=lambda x: x['score'])
    
    return {"emoción_principal": max_emotion}
    

@app.post("/classify", summary="Clasificar Texto", description="Clasifica el texto proporcionado en compromiso, duda, acuerdo o desacuerdo con porcentajes.")
async def classify_text(request: ClassificationRequest):
    text = request.texto.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Crear una instancia del cliente de OpenAI
    openai_client = OpenAI(api_key=api_key)


    # Crear el mensaje para enviar al ChatBot
    message = [
        {
            "role": "system",
            "content": "Dado el siguiente texto, clasifícalo en una de las siguientes categorías: 'Compromiso', 'Duda', 'Acuerdo', 'Desacuerdo', o 'Texto Libre' y dime con porcentajes cuánto corresponde a cada categoría en el formato 'compromiso: 0%, duda: 0%, acuerdo: 0%, desacuerdo: 0%, texto libre: 0%'.\n\n1. Compromiso: Indica una promesa o una declaración de intención.\n2. Duda: Expresa incertidumbre o pregunta sobre algo.\n3. Acuerdo: Muestra conformidad o aceptación de una idea.\n4. Desacuerdo: Manifiesta una opinión contraria a una idea.\n5. Texto Libre: Cualquier texto que no se clasifique en las categorías anteriores.\n\nEjemplos:\n\nTexto: 'Voy a enviar el informe mañana.'\nCategoría: Compromiso\n\nTexto: '¿Estás seguro de esto?'\nCategoría: Duda\n\nTexto: 'Estoy de acuerdo con lo que dijiste.'\nCategoría: Acuerdo\n\nTexto: 'No creo que eso funcione.'\nCategoría: Desacuerdo\n\nTexto: 'El clima hoy es agradable.'\nCategoría: Texto Libre\n\nTexto: 'Leí tu mensaje.'\nCategoría: Texto Libre"
        }
    ]

    # Agregar la entrada del usuario al mensaje
    message.append({"role": "user", "content": text})

    # Obtener la respuesta del ChatBot
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
    )

    # Obtener la respuesta del ChatBot
    assistant_response = completion.choices[0].message.content

    # Separar la respuesta en categorías y porcentajes
    response_parts = assistant_response.split(', ')
    categories = []
    percentages = []

    for part in response_parts:
        category, percentage = part.split(': ')
        categories.append(category.strip())
        percentages.append(int(percentage.strip('%')))

    # Crear un diccionario con las categorías y porcentajes
    result = dict(zip(categories, percentages))

    return result

# Define el endpoint para analilar dos posturas en desacuerdos
@app.post("/desacuerdos", summary="Analizar Desacuerdo", description="Analiza dos posturas en un desacuerdo y determina si son opuestas o no.")
async def analyze_disagreement(request: ClassificationRequest):
    text = request.texto.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Crear una instancia del cliente de OpenAI
    openai_client = OpenAI(api_key=api_key)

    # Crear el mensaje para enviar al ChatBot
    message = [
        {
            "role": "system",
            "content": "Indica cuales son las dos posturas en desacuerdo en el formato 'postura1: postura2"
        }
    ]

    # Agregar la entrada del usuario al mensaje
    message.append({"role": "user", "content": text})

    # Obtener la respuesta del ChatBot
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
    )

    # Obtener la respuesta del ChatBot
    assistant_response = completion.choices[0].message.content

    # Verificar si se proporcionaron ambas posturas en la respuesta del asistente
    posturas = assistant_response.split(":")
    if len(posturas) != 2:
        return {"error": "Debes proporcionar exactamente dos posturas en desacuerdo separadas por ':'"}

    # Guardar las posturas como postura1 y postura2 
    postura1 = posturas[0].strip()
    postura2 = posturas[1].strip()

    # retornar las posturas
    return {"postura1": postura1, "postura2": postura2}
    

# Define el endpoint para analilar y crear un compromiso
@app.post("/compromiso", summary="Crear Compromiso", description="Crea un compromiso a partir de las condiciones de sasticfacción")
async def create_commitment(request: ClassificationRequest):
    text = request.texto.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Crear una instancia del cliente de OpenAI
    openai_client = OpenAI(api_key=api_key)

    # Crear el mensaje para enviar al ChatBot
    message = [
        {
            "role": "system",
            "content": (
                "Voy a proporcionarte una frase de compromiso y quiero que la descompongas en un formato JSON con las claves: "
                "'quién', 'qué', 'cuándo', y 'dónde'. Si alguna parte falta, déjala como una cadena vacía. "
                "Ejemplo de entrada: 'Juan va a hacer cambio en la base de datos mañana en la oficina'. "
                "Ejemplo de salida: {\"quién\": \"Juan\", \"qué\": \"va a hacer cambio en la base de datos\", \"cuándo\": \"mañana\", \"dónde\": \"la oficina\"}."
            )
        }
    ]

    # Agregar la entrada del usuario al mensaje
    message.append({"role": "user", "content": text})

    # Obtener la respuesta del ChatBot
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message
    )

    # Obtener la respuesta del ChatBot
    assistant_response = completion.choices[0].message.content
    print(assistant_response)

    # Parsear la respuesta como JSON
    try:
        data = json.loads(assistant_response)
        compromiso = {
            "quién": data.get("quién", "[[quién]]"),
            "qué": data.get("qué", "[[qué]]"),
            "cuándo": data.get("cuándo", "[[cuándo]]"),
            "dónde": data.get("dónde", "[[dónde]]")
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="La respuesta del modelo no es un JSON válido")

   # Verificar y asignar valores predeterminados si los campos están vacíos
    compromiso['quién'] = "[Quien]" if not compromiso['quién'] else compromiso['quién']
    compromiso['qué'] = "[Que]" if not compromiso['qué'] else compromiso['qué']
    compromiso['cuándo'] = "[Cuando]" if not compromiso['cuándo'] else compromiso['cuándo']
    compromiso['dónde'] = "[Donde]" if not compromiso['dónde'] else compromiso['dónde']

    # Construir el texto del compromiso
    compromiso_texto = f"{compromiso['quién']} {compromiso['qué']} {compromiso['cuándo']} en {compromiso['dónde']}."

    return {"compromiso": compromiso_texto}

