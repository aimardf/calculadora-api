# Imagen base ligera con Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /code

# Primero las dependencias (así Docker las cachea entre builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código de la API
COPY app ./app

# Puerto en el que escucha uvicorn
EXPOSE 8000

# Arranca la API. 0.0.0.0 = acepta conexiones desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
