import requests
from flask import Blueprint, jsonify, current_app


# Define the Blueprint
stock_value_bp = Blueprint('stock-value', __name__)


@stock_value_bp.route('/<string:id>', methods=['GET'])
def get_stock_value(id):
    API_KEY = stock_value_bp.API
    stock_collection = stock_value_bp.stock_collection
    try:
        cur_stock = stock_collection.find_one({'id': id})
        if cur_stock is None:
            return jsonify({'error': "Not found"}), 404
        symbol = cur_stock.get('symbol')

        api_url = f'https://api.api-ninjas.com/v1/stockprice?ticker={symbol}'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            if response.json():
                stock_current_price = response.json().get('price')
                stock_value = round(stock_current_price * cur_stock['shares'], 2)
                return jsonify({
                    'symbol': symbol,
                    'ticker': stock_current_price,
                    'stock value': stock_value
                }), 200
            else:
                return jsonify({"error": "Not found"}), 404
        else:
            return jsonify({"server error": "API response code " + str(response.status_code)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
