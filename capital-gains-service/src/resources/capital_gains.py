import common.common as res
import requests
from flask import Blueprint, jsonify, request

capital_gains_bp = Blueprint('capital-gains', __name__)
STOCK_VALUE_API = "http://127.0.0.1:8000/stock-value/"
VALID_QUERY = ["portfolio", "numsharesgt", "numshareslt"]

@capital_gains_bp.route('/', methods=['GET'])
def get_capital_gains():
    try:
        query_params = request.args.to_dict()
        if not query_params:
            return jsonify({"capital gains": capital_gains_no_query()}), 200
        else:
            return capital_gains_query(query_params)

    except Exception as e:
        return res.server_error_res(e)


def capital_gains_no_query():
    portfolio_stocks = list(capital_gains_bp.stock1_collection.find()) + list(capital_gains_bp.stock2_collection.find())
    capital_gain = calculate_capital_gain(portfolio_stocks)
    return capital_gain


def capital_gains_query(query_params: dict):
    for query in query_params.keys():
        if query not in VALID_QUERY:
            return res.malformed_res()

    capital_gains = list(capital_gains_bp.stock1_collection.find()) + list(capital_gains_bp.stock2_collection.find())

    if "portfolio" in query_params:
        if query_params["portfolio"] == "stocks1":
            capital_gains = list(capital_gains_bp.stock1_collection.find())
        elif query_params["portfolio"] == "stocks2":
            capital_gains = list(capital_gains_bp.stock2_collection.find())
        else:
            return res.malformed_res()

    if "numsharesgt" in query_params:
        try:
            numsharesgt = int(query_params["numsharesgt"])
            capital_gains = [
                stock for stock in capital_gains if stock.get("shares", 0) > numsharesgt
            ]
        except ValueError:
            return res.malformed_res()

    if "numshareslt" in query_params:
        try:
            numshareslt = int(query_params["numshareslt"])
            capital_gains = [
                stock for stock in capital_gains if stock.get("shares", 0) < numshareslt
            ]
        except ValueError:
            return res.malformed_res()

    return jsonify({"capital gains": calculate_capital_gain(capital_gains)}), 200


def calculate_capital_gain(portfolio_stocks: list):
    capital_gain = 0
    for stock in portfolio_stocks:
        id = stock["id"]
        response = requests.get(f"{STOCK_VALUE_API}{id}")
        data = response.json()
        capital_gain += data["stock value"] - stock["purchase_price"] * stock["shares"]

    return capital_gain




