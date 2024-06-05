# TextEdit API

API para análisis de sentimientos y emociones en texto.

## Requisitos

-   Python 3.7 o superior
-   Una máquina virtual (VM) para ejecutar la API

## Instalación

1.  Clona este repositorio en tu máquina virtual:

`git clone https://github.com/dmeetflow/TextEdit-API.git` 

2.  Navega hasta el directorio del proyecto:

`cd TextEdit-API` 

3.  Instala las dependencias usando pip:

`pip install -r requirements.txt` 

## Uso

1.  Inicia el servidor de desarrollo con el siguiente comando:

`uvicorn main:app --reload` 

2.  La API estará disponible en `http://localhost:8000`.

## Endpoints

### Saludo y Enlace a la Documentación

-   **URL**: `/`
-   **Método HTTP**: GET
-   **Descripción**: Proporciona un enlace directo a la documentación de la API para obtener más información sobre los endpoints disponibles y su uso.

### Analizar Sentimiento

-   **URL**: `/sentiment`
-   **Método HTTP**: POST
-   **Descripción**: Analiza el sentimiento del texto proporcionado.
-   **Datos de entrada (JSON)**:
    
    `{
        "text": "Texto a analizar"
    }` 
    
-   **Datos de salida (JSON)**:
    
    `{
        "sentiment": "POSITIVO/NEGATIVO",
        "score": 0.9
    }` 
    

### Analizar Emociones

-   **URL**: `/emotions`
-   **Método HTTP**: POST
-   **Descripción**: Analiza las emociones en un texto en español.
-   **Datos de entrada (JSON)**:
    
    `{
        "texto": "Texto a analizar"
    }` 
    
-   **Datos de salida (JSON)**:
    
    `{
        "emoción_principal": "Emoción"
    }` 
    

### Clasificar Texto

-   **URL**: `/classify`
-   **Método HTTP**: POST
-   **Descripción**: Clasifica el texto proporcionado en compromiso, duda, acuerdo o desacuerdo con porcentajes.
-   **Datos de entrada (JSON)**:
        
    `{
        "texto": "Texto a clasificar"
    }` 
    
-   **Datos de salida (JSON)**:

    `{
        "compromiso": 0,
        "duda": 25,
        "acuerdo": 50,
        "desacuerdo": 25
    }` 
    

### Obtener Información de Elemento

-   **URL**: `/infoElement`
-   **Método HTTP**: POST
-   **Descripción**: Obtiene la fecha, el lugar y la descripción de un elemento en un formato específico.
-   **Datos de entrada (JSON)**:

    
    `{
        "texto": "Texto a analizar"
    }` 
    
-   **Datos de salida (JSON)**:
        
    `{
        "Fecha": "dd/mm/yyyy HH:MM",
        "Lugar": "Lugar",
        "QueSeRealiza": "Realización"
    }`