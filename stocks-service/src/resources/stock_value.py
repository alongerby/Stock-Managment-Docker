from config import stockDB, API_KEY
import requests
from flask import Blueprint, jsonify

# Define the Blueprint
stock_value_bp = Blueprint('stock-value', __name__)


@stock_value_bp.route('/<string:id>', methods=['GET'])
def get_stock_value(id):
    try:
        curStock = next((stock for stock in stockDB if stock['id'] == id), None)

        if curStock is None:
            return jsonify({'error': "Not found"}), 404

        symbol = curStock.get('symbol')

        api_url = f'https://api.api-ninjas.com/v1/stockprice?ticker={symbol}'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            if response.json():
                stockCurrentPrice = response.json().get('price')
                stockValue = round(stockCurrentPrice * curStock['shares'], 2)
                return jsonify({
                    'symbol': symbol,
                    'ticker': stockCurrentPrice,
                    'stock value': stockValue
                }), 200
            else:
                return jsonify({"error": "Not found"}), 404
        else:
            return jsonify({"server error": "API response code " + str(response.status_code)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
