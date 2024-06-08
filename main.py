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

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(title="TextEdit API", description="API para análisis de sentimientos y emociones en texto.")

# Cargar el pipeline de transformers para análisis de sentimientos
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
# Carga del modelo para análisis de emociones
classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", top_k=None)

# Configuración del cliente de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Configuración de CORS
origins = [
    "http://localhost:3001",
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

    # Encuentra la emoción con el mayor puntaje
    max_emotion = max(simplified_prediction, key=lambda x: x['score'])
    
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
            "content": "Indifico si es un compromiso, una duda, un acuerdo o un desacuerdo y dime con porcentajes cuanto corresponde en cada categoria en el formato 'compromiso: 0%, duda: 0%, acuerdo: 0%, desacuerdo: 0%'"
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


@app.post("/infoElement", summary="Obtener Información de Elemento", description="Obtiene la fecha, el lugar y la descripción de un elemento en un formato específico.")
async def get_element_info(request: ElementInfoRequest):
    text = request.texto.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    # Crear una instancia del cliente de OpenAI
    openai_client = OpenAI(api_key=api_key)

    # Crear el mensaje para enviar al ChatBot
    message = [
        {
            "role": "system",
            "content": "rellena los datos siguiendo este formato: {Fecha: dd/mm/yyyy HH:MM, Lugar: lugar, QueSeRealiza: Realizacion} en caso que un valor no se encuentre dejarlo en blanco"
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
    # Limpiar la respuesta eliminando las llaves adicionales
    assistant_response = assistant_response.replace("{", "").replace("}", "")

    print (assistant_response)
    # se obtiene :{Fecha: 23/11/2021, Lugar: Centro, QueSeRealiza: trabajar en el Banco del Tiempo}

    # Separar la respuesta en categorías e informacion
    
    response_parts = assistant_response.split(', ')
    categories = []
    information = []

    for part in response_parts:
        category, info = part.split(': ')
        categories.append(category.strip())
        information.append(info.strip())

    # Crear un diccionario con las categorías y porcentajes
    result = dict(zip(categories, information))

    return result

    

    
