from datetime import datetime
from flask import Blueprint, jsonify, requests

portfolio_value_bp = Blueprint('portfolio-value', __name__)


@portfolio_value_bp.route('/', methods=['GET'])
def get_portfolio_value():
    try:
        portfolio_value = 0
        for stock in stockDB:
            symbol = stock['symbol']
            api_url = f'https://api.api-ninjas.com/v1/stockprice?ticker={symbol}'
            response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
            if response.status_code == requests.codes.ok:
                if response.json():
                    portfolio_value += response.json().get('stock value')
            else:
                return jsonify({"server error": "API response code " + str(response.status_code)}), 500
        return jsonify({
            "date": datetime.now().strftime("%d-%m-%Y"),
            "portfolio_value": portfolio_value
        })
    except Exception as e:
        return jsonify({"server error": str(e)}), 500
