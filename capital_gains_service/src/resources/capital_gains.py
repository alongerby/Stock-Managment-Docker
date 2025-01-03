import common.common as res
import requests
from flask import Blueprint, jsonify, request

capital_gains_bp = Blueprint('capital-gains', __name__)
stock1_value_api = "http://nginx:8081/stocks1/stock-value/"
stock2_value_api = "http://stocks2:8000/stock-value/"
VALID_QUERY = ["portfolio", "numsharesgt", "numshareslt"]

@capital_gains_bp.route('/', methods=['GET'])
def get_capital_gains():
    try:
        query_params = request.args.to_dict()
        if not query_params:
            return jsonify(capital_gains_no_query()), 200
        else:
            return capital_gains_query(query_params)

    except Exception as e:
        return res.server_error_res(e)


def capital_gains_no_query():
    capital_gains = {
        "stocks1": list(capital_gains_bp.stock1_collection.find()),
        "stocks2": list(capital_gains_bp.stock2_collection.find())
    }
    capital_gain_sum = (calculate_capital_gain(capital_gains["stocks1"], stock1_value_api) +
                        calculate_capital_gain(capital_gains["stocks2"], stock2_value_api))
    return capital_gain_sum


def capital_gains_query(query_params: dict):
    for query in query_params.keys():
        if query not in VALID_QUERY:
            return res.malformed_res()

    capital_gains = {
        "stocks1": list(capital_gains_bp.stock1_collection.find()),
        "stocks2": list(capital_gains_bp.stock2_collection.find())
    }

    if "portfolio" in query_params:
        if query_params["portfolio"] == "stocks1":
            capital_gains = {"stocks1": capital_gains["stocks1"], "stocks2": []}
        elif query_params["portfolio"] == "stocks2":
            capital_gains = {"stocks1": [], "stocks2": capital_gains["stocks2"]}
        else:
            return res.malformed_res()

    if "numsharesgt" in query_params:
        try:
            numsharesgt = int(query_params["numsharesgt"])
            for key in capital_gains:
                capital_gains[key] = [
                    stock for stock in capital_gains[key] if stock.get("shares", 0) > numsharesgt
                ]
        except ValueError:
            return res.malformed_res()

    if "numshareslt" in query_params:
        try:
            numshareslt = int(query_params["numshareslt"])
            for key in capital_gains:
                capital_gains[key] = [
                    stock for stock in capital_gains[key] if stock.get("shares", 0) < numshareslt
                ]
        except ValueError:
            return res.malformed_res()

    capital_gain_sum = (calculate_capital_gain(capital_gains["stocks1"], stock1_value_api) +
                        calculate_capital_gain(capital_gains["stocks2"], stock2_value_api))

    return jsonify(capital_gain_sum), 200


def calculate_capital_gain(portfolio_stocks: list, api_uri: str):
    capital_gain = 0
    for stock in portfolio_stocks:
        id = stock["id"]
        response = requests.get(f"{api_uri}{id}")
        data = response.json()
        capital_gain += data["stock value"] - stock["purchase price"] * stock["shares"]

    return round(capital_gain, 2)




