# Usa una imagen base de Python ligera
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Crea el directorio donde se almacenará la base de datos
RUN mkdir -p /data
RUN chmod 777 /data

# Copia el resto de los archivos del proyecto a /app
COPY . .

# Expone el puerto 5002 para acceder a la API Flask
EXPOSE 5002

# Inicializa la base de datos y ejecuta la aplicación Flask
CMD ["sh", "-c", "python init_db.py && python app.py"]