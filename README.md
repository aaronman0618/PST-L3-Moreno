# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.  
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.  
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows

Desde backend, en una terminal Command Prompt de VS Code:

```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger: http://127.0.0.1:8000/docs

En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.  
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo 100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.  
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.  
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación: utilizar únicamente en la red de laboratorio autorizada.

## Firmware

Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.  
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.  
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.  
No publicar config.h, contraseñas ni tokens.

## Reto

Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.  
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).  
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Antes de la sesión

El docente debe probar el firmware en el hardware real y la red del aula, precargar las herramientas y validar las dependencias en los equipos.  
La guía destina 105 minutos a trabajar con el entorno ya preparado.

## Desarrollo de la práctica

**Estudiante:** Aarón Augusto Moreno Alarcón  
**Paralelo:** 104

### Objetivo

Comprender la estructura de un backend desarrollado con FastAPI, probar sus endpoints mediante Swagger y agregar una ruta que permita calcular los promedios de temperatura y humedad.

### Modificaciones realizadas

Se modificó `routes.py` para agregar el campo `"laboratorio": 3` en la respuesta de `GET /salud`.

Se implementó el endpoint `GET /lecturas/promedio` mediante cambios en `routes.py` y `services.py`. Esta función calcula los promedios de las últimas lecturas disponibles, utilizando un parámetro `n` entre 1 y 100, con valor predeterminado de 3.

### Preguntas de comprensión

**Pregunta 1. ¿Qué función recibe el JSON y cuál lo guarda?**

La función `post_lectura()` recibe los datos y `guardar_lectura()` los almacena en `store.lecturas`.

**Pregunta 2. ¿Qué archivo cambiarías para añadir una URL?**

El archivo `routes.py`, porque contiene las rutas de la API.

**Pregunta 3. ¿Qué ocurre con las lecturas y el color cuando se reinicia la API? ¿Por qué?**

Las lecturas se eliminan y el color vuelve a apagado porque los datos se almacenan temporalmente en memoria.

**Pregunta 4. ¿Por qué una petición con JSON bien escrito puede devolver 422? Indica qué archivo define esa validación.**

Porque los valores pueden incumplir las restricciones definidas en `schemas.py`, aunque el JSON tenga una estructura correcta.

**Pregunta 5. ¿Cuál es el recorrido de una lectura y cuándo cambia el LED?**

El ESP8266 envía una petición POST al backend. La ruta recibe los datos, el modelo los valida, el servicio los guarda en memoria y devuelve una respuesta con el color del LED. El LED físico cambia cuando el ESP8266 recibe y aplica ese color.

### Resultados de las pruebas originales

| Método y ruta | Código esperado | Código obtenido |
|---|---|---|
| GET /salud | 200 | 200 |
| GET /lecturas | 200 | 200 |
| GET /led | 200 | 200 |
| PUT /led (verde) | 200 | 200 |
| POST /lecturas (válida) | 201 | 201 |
| GET /lecturas (después del POST) | 200 | 200 |
| GET /led (después del PUT) | 200 | 200 |
| POST /lecturas (humedad 150) | 422 | 422 |
| PUT /led (amarillo) | 422 | 422 |

### Resultados del endpoint de promedios

Se utilizaron las siguientes lecturas:

| Lectura | Temperatura | Humedad |
|---|---|---|
| 1 | 20 | 40 |
| 2 | 24 | 50 |
| 3 | 28 | 60 |

| Consulta | Código esperado | Código obtenido | Resultado |
|---|---|---|---|
| Sin lecturas, n=3 | 404 | 404 | No hay lecturas disponibles |
| n=3 | 200 | 200 | Cantidad 3; temperatura 24; humedad 50 |
| n=2 | 200 | 200 | Cantidad 2; temperatura 26; humedad 55 |
| n=5 | 200 | 200 | Cantidad 3; temperatura 24; humedad 50 |
| n=0 | 422 | No ejecutado | Swagger rechaza valores inferiores a 1 |
| n=101 | 422 | No ejecutado | Swagger rechaza valores superiores a 100 |
| Sin indicar n | 200 | 200 | Cantidad 3; temperatura 24; humedad 50 |

### Observación

Las lecturas se almacenan temporalmente en memoria, por lo que desaparecen al reiniciar el backend. El endpoint de promedios utiliza las últimas lecturas disponibles y devuelve la cantidad realmente utilizada.