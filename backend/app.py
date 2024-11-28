from flask import Flask, request, jsonify, render_template
import requests
import redis
import json
import os  


url_convert = "https://v6.exchangerate-api.com/v6/a6b6b66db857e66ab5dd506b/pair"

data_api_url = "http://db:5002/data"

# Inicializa Redis
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0)
    redis_available = True
except redis.ConnectionError:
    redis_available = False

app = Flask(__name__)


@app.route("/tax")
def obtaintax():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    if not from_currency or not to_currency:
        return "<h1>Parámetros 'from' y 'to' son requeridos.</h1>", 400

    fetch_url = url_convert + "/" + from_currency + "/" + to_currency
    response = requests.get(fetch_url)
    
    if response.status_code == 200:
        tax = response.json()
        exchange_rate = float(tax.get("conversion_rate"))
        
        container_id = os.getenv("HOSTNAME", "Unknown container")
        return f"<h1>Tasa de cambio {from_currency}-{to_currency} está en: {exchange_rate}</h1>"
        
    else:
        return f"<h1>Error en la solicitud: {response.status_code}</h1>", response.status_code


@app.route("/rates")
def home():
    data = None

    # Intenta obtener los datos de Redis dinámicamente
    try:
        cached_data = redis_client.get("api_response")
        
        if cached_data:
            print("Datos obtenidos de Redis")
            data = json.loads(cached_data)

            # Verifica si `data` es un diccionario antes de agregar "source"
            if isinstance(data, dict):
                data["source"] = "Redis"
            elif isinstance(data, list) and len(data) > 0:
                data[0]["source"] = "Redis"

            return jsonify(data)

    except redis.ConnectionError:
        print("Redis no está disponible. Continuando sin caché.")
    except Exception as e:
        print(f"No se pudo recuperar datos de Redis: {e}")

    # Si no existen en Redis o Redis no está disponible, realiza la solicitud a la API
    response = requests.get(data_api_url)
    if response.status_code == 200:
        data = response.json()

        # Añade la información de la fuente
        if isinstance(data, dict):
            data["source"] = "MySqlite"
        elif isinstance(data, list) and len(data) > 0:
            data[0]["source"] = "MySqlite"

        # Guarda los datos en Redis si está disponible
        try:
            redis_client.setex("api_response", 3600, json.dumps(data))
            print("Datos obtenidos de la API y guardados en Redis")
        except redis.ConnectionError:
            print("No se pudo guardar los datos en Redis. Redis no está disponible.")

        return jsonify(data)
    else:
        return f"Error en la solicitud: {response.status_code}", response.status_code

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.json.get('from')
    to_currency = request.json.get('to')
    amount = request.json.get('amount')
    
    fetch_url = url_convert + "/" + from_currency + "/" + to_currency
    response = requests.get(fetch_url)
    
    if response.status_code == 200:
        tax = response.json()
        exchange_rate = float(tax.get("conversion_rate"))
        converted_amount = float(amount) * exchange_rate
        
        print(f"datos:{exchange_rate}")
        container_id = os.getenv("HOSTNAME", "Unknown container")
        return jsonify({
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "exchange_rate": exchange_rate,
            "from_currency": from_currency,
            "to_currency": to_currency,
	    "id_backend": container_id
        })
        
    else:
        return f"<h1>Error en la solicitud: {response.status_code}</h1>", response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
