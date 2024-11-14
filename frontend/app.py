from flask import Flask, request, jsonify,render_template
import requests, sqlite3
app = Flask(__name__)

url_backend="http://backend:5000/rates"
url_backend_convert="http://backend:5000/convert"



@app.route('/rates', methods=['GET'])
def receive_data():
    # funcionalidad de /rates?from=USD&to=EUR
    # prueba: http://localhost:5001/rates?from=USD&to=ARS&amount=100
    from_currency = request.args.get("from", default="USD")  # Valor por defecto USD
    to_currency = request.args.get("to", default="USD")      # Valor por defecto USD
    amount = request.args.get("amount", default=0.0, type=float)  # Valor por defecto 0.0
    
    try:
        # Obtener los datos de las tasas de cambio del backend
        response = requests.get(url_backend)
        
        if response.status_code == 200:
            data = response.json()
            conversion_rates = data
            # Renderizar la plantilla y pasarle los parámetros para preseleccionar los valores
            return render_template("index.html", data=conversion_rates, 
                                   from_currency=from_currency, 
                                   to_currency=to_currency, 
                                   amount=amount)
        else:
            print(f"Error al hacer la solicitud: {response.status_code}")
            return f"Error al hacer la solicitud: {response.status_code}", response.status_code
    
    except requests.RequestException as e:
        return jsonify({"error": "Failed to retrieve data"}), 500

 
 
 
@app.route('/convert', methods=['POST'])
def convert_data():   
    try:
        from_currency = request.form.get('from')
        to_currency = request.form.get('to')
        amount = request.form.get('amount')
        
        payload = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        # Realiza la solicitud POST al servicio de conversión
        response = requests.post(url_backend_convert, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"datos:{data}")
            return render_template("result.html",data=data)
        
        else:
            print(f"Error al hacer la solicitud: {response.status_code}")
            return render_template("result.html", error="Error al hacer la solicitud")
        
    except requests.RequestException as e:
        return jsonify({"error": "Failed to retrieve data"}), 500
 


 
@app.route('/', methods=['GET'])
def index():
    return render_template("ini.html")


def query_strings():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = request.args.get("amount")
    print(f"Peticion enviada: {from_currency} {to_currency} {amount}")

if __name__ == '__main__':
    app.add_url_rule("/rates",view_func=query_strings)
    app.run(port=5001)