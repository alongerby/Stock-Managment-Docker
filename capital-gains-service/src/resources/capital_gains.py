import logging
import uuid
import common.common as res
import requests
from flask import Blueprint, jsonify, request, current_app

capital_gains_bp = Blueprint('stocks', __name__)
# stock_collection = current_app.config["COLLECTION"]
STOCK_VALUE_API = "http://127.0.0.1:8000/stock-value/"
VALID_QUERY = ["portfolio", "numsharesgt", "numshareslt"]

@capital_gains_bp.route('/', methods=['GET'])
def get_capital_gains():
    try:
        query_params = request.args.to_dict()
        if not query_params:
            return jsonify({"capital gains":capital_gains_no_query()}), 200

    except Exception as e:
        return res.server_error_res(e)


def capital_gains_no_query():
    portfolio_stocks = capital_gains_bp.stock_collection.find()
    capital_gain = 0
    for stock in portfolio_stocks:
        id = stock["id"]
        response = requests.get(f"{STOCK_VALUE_API}{id}")
        print(response)
        data = response.json()
        capital_gain += data["stock value"] - stock["purchase_price"] * stock["shares"]
    return capital_gain


def capital_gains_query(query_params: dict):
    for query in query_params.keys():
        if query not in VALID_QUERY:
            return res.malformed_res()


