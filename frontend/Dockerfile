# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt a /app
COPY requirements.txt .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación a /app
COPY . .

# Expone el puerto 80 para el frontend
EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]