# TextEdit API
API para análisis de sentimientos y emociones en texto.

## Requisitos

- Python 3.7 o superior
- Una máquina virtual (VM) para ejecutar la API

1.  Instala la biblioteca `virtualenv` si aún no lo has hecho. Por ejemplo, en Windows puedes usar:
`python -m venv venv`
`venv\Scripts\activate`

## Instalación
1. Clona este repositorio en tu máquina virtual:
`git clone https://github.com/dmeetflow/API-TextEdit.git`
2. Navega hasta el directorio del proyecto:
`cd API-TextEdit`
3. Instala las dependencias usando pip:
`pip install -r requirements.txt`
## Uso
1. Inicia el servidor de desarrollo con el siguiente comando:
`uvicorn main:app --reload`

2. La API estará disponible en `http://localhost:8000`.

## Endpoints

### Saludo y Enlace a la Documentación

-  **URL**: `/`

-  **Método HTTP**: GET

-  **Descripción**: Proporciona un enlace directo a la documentación de la API para obtener más información sobre los endpoints disponibles y su uso.

### Analizar Sentimiento

-  **URL**: `/sentiment`

-  **Método HTTP**: POST

-  **Descripción**: Analiza el sentimiento del texto proporcionado.

-  **Datos de entrada (JSON)**:

		{

			"text": "Texto a analizar"

		}

-  **Datos de salida (JSON)**:

	

	    {
    
	    	"sentiment": "POSITIVO/NEUTRAL/NEGATIVO",
	    
	    	"score": 0.9
    
    	}

### Analizar Emociones

-  **URL**: `/emotions`

-  **Método HTTP**: POST

-  **Descripción**: Analiza las emociones en un texto en español.

-  **Datos de entrada (JSON)**:

	    {
	    
		    "texto": "Texto a analizar"
	    
	    }

-  **Datos de salida (JSON)**:

	    {
	    
	    "emoción_principal":  {
	    
		    "label":  "joy",
	    
		    "score":  0.9
	    
		    }
	    
	    }

  

### Clasificar Texto

  

-  **URL**: `/classify`

-  **Método HTTP**: POST

-  **Descripción**: Clasifica el texto proporcionado en compromiso, duda, acuerdo o desacuerdo con porcentajes.

-  **Datos de entrada (JSON)**:

		{

			"texto": "Texto a clasificar"

		}

-  **Datos de salida (JSON)**:

  

		{

			"compromiso": 0,

			"duda": 25,

			"acuerdo": 50,

			"desacuerdo": 25

		}

  

### Obtener Información de Elemento Acuerdo
  
-  **URL**: `/compromiso`

-  **Método HTTP**: POST

-  **Descripción**: Obtiene las condiciones de satisfacción y redacta un compromiso.

-  **Datos de entrada (JSON)**:

		{

			"texto": "Texto a analizar"

		}`

-  **Datos de salida (JSON)**:

		{

		"compromiso":  "[Quien] Estudiar al menos dos horas todos los días [Cuando] en [Donde]."

		}


### Obtener Información de Elemento Desacuerdo

  

-  **URL**: `/desacuerdos`

-  **Método HTTP**: POST

-  **Descripción**: Obtiene las dos posturas que se encuentran en un desacuerdo.

-  **Datos de entrada (JSON)**:

		{

			"texto": "Texto a analizar"

		}`

-  **Datos de salida (JSON)**:

		{

			"postura1":  "postura1",

			"postura2":  "postura2"

		}



## Ejecutar Pruebas Unitarias

Para ejecutar las pruebas unitarias, asegúrate de tener instalada la biblioteca `pytest` en tu entorno virtual o globalmente. Si no lo has hecho, puedes instalarlo con el siguiente comando:

`pip install pytest`

Una vez que tengas instalado `pytest`, simplemente navega hasta el directorio donde se encuentra el archivo `test_api.py` y ejecuta el siguiente comando en tu terminal:

`pytest`

Esto ejecutará todas las pruebas definidas en el archivo `test_api.py` y te mostrará un resumen de los resultados. Si todas las pruebas pasan correctamente, verás un mensaje indicando que todas las pruebas han pasado.
