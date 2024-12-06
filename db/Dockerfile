# Usa una imagen base de Python ligera
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto a /app
COPY . .

RUN python init_db.py

# Expone el puerto 5001 para acceder a la API Flask
EXPOSE 5002
# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]