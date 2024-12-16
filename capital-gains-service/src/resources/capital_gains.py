import uuid
from flask import Blueprint, jsonify, request, current_app

captial_gains_bp = Blueprint('stocks', __name__)
stock_collection = current_app.config["COLLECTION"]


@captial_gains_bp.route('/', methods=['GET'])
def get_capital_gains():
    try:
        query_params = request.args.to_dict()
        if not query_params:
            capital_gains_no_query()

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


def capital_gains_no_query():


