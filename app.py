from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Tu API Key de ExchangeRate API
API_KEY = 'be888a2659792c5d5be23e88'

@app.route('/')
def index():
    # Obtener las divisas disponibles desde la API
    url_codes = f'https://v6.exchangerate-api.com/v6/{API_KEY}/codes'
    response_codes = requests.get(url_codes)
    data_codes = response_codes.json()

    if response_codes.status_code == 200 and data_codes['result'] == 'success':
        currencies = data_codes['supported_codes']  # Lista de divisas en formato [['USD', 'Dólar Estadounidense'], ...]
    else:
        currencies = [['USD', 'Dólar Estadounidense'], ['EUR', 'Euro'], ['GBP', 'Libra Esterlina'], ['JPY', 'Yen Japonés']]  # Divisas por defecto

    # Obtener las tasas de cambio para las divisas seleccionadas
    url_rates = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response_rates = requests.get(url_rates)
    data_rates = response_rates.json()

    if response_rates.status_code == 200 and data_rates['result'] == 'success':
        exchange_rates = data_rates['conversion_rates']
    else:
        exchange_rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.25,
            'AUD': 1.35,
            'CAD': 1.26,
            'CHF': 0.92,
            'CNY': 6.45,
            'MXN': 20.50,  # Tasa de cambio aproximada del MXN
            'NZD': 1.42
        }  # Tasas de cambio por defecto

    # Seleccionar 10 divisas populares para mostrar en las tarjetas
    selected_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'MXN', 'NZD']
    currency_cards = []
    for code in selected_currencies:
        if code in exchange_rates:
            currency_cards.append({
                'code': code,
                'name': next((name for c, name in currencies if c == code), code),
                'rate': exchange_rates[code]
            })

    return render_template('index.html', currencies=currencies, currency_cards=currency_cards)

@app.route('/convertir', methods=['POST'])
def convertir():
    # Obtener datos del formulario
    amount = float(request.form['amount'])
    from_currency = request.form['fromCurrency']
    to_currency = request.form['toCurrency']

    # Hacer la solicitud a la API
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['result'] == 'success':
        # Obtener la tasa de cambio
        exchange_rate = data['conversion_rates'][to_currency]
        # Calcular el monto convertido
        converted_amount = amount * exchange_rate
        # Devolver el resultado como JSON
        return jsonify({
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'converted_amount': round(converted_amount, 2),
            'exchange_rate': exchange_rate
        })
    else:
        return jsonify({'error': 'No se pudo obtener la tasa de cambio'}), 400
  
if __name__ == '__main__':
    app.run(debug=True)