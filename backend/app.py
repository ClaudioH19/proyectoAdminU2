from flask import Flask, request, jsonify, render_template
import requests
url_convert = "https://v6.exchangerate-api.com/v6/a6b6b66db857e66ab5dd506b/pair"

data_api_url = "http://db:5002/data"

app = Flask(__name__)

@app.route("/rates")
def home():
    response = requests.get(data_api_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return jsonify(data)
    else:
        return f" Error en la solicitud: {response.status_code}", response.status_code



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
        
        return jsonify({
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "exchange_rate": exchange_rate,
            "from_currency": from_currency,
            "to_currency": to_currency
        })
        
    else:
        return f"<h1>Error en la solicitud: {response.status_code}</h1>", response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
