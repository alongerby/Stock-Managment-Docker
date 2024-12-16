from datetime import datetime
import uuid
from flask import Blueprint, jsonify, request, current_app

stocks_bp = Blueprint('stocks', __name__)
stock_collection = current_app.config["COLLECTION"]


@stocks_bp.route('/', methods=['GET'])
def get_stocks():
    try:
        query_params = request.args.to_dict()
        if not query_params:
            return stock_collection.find(), 200

        filtered_stocks = []

        for field, value in query_params.items():
            filtered_stocks = filtered_stocks + list(stock_collection.find({field: value}))

        return jsonify(filtered_stocks), 200

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/', methods=['POST'])
def create_stock():
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415

        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Malformed data"}), 400

        required_fields = ['symbol', 'purchase_price', 'shares']

        for field in required_fields:
            if field not in payload:
                return jsonify({"error": "Malformed data"}), 400

        if stock_collection.find_one({'symbol': payload['symbol']}):
            return jsonify({"error": "Malformed data"}), 400

        if not isinstance(payload['symbol'], str) or not isinstance(payload['purchase_price'],
                                                                    (int, float)) or not isinstance(payload['shares'],
                                                                                                    int):
            return jsonify({"error": "Malformed data"}), 400

        stock_id = str(uuid.uuid4())
        name = payload.get('name', 'NA')
        purchase_date = payload.get('purchase_date', 'NA')
        if not validate_date(purchase_date):
            return jsonify({"error": "Malformed data"}), 400

        stock = {
            'id': stock_id,
            'symbol': payload['symbol'].upper(),
            'purchase_price': round(payload['purchase_price'], 2),
            'shares': payload['shares'],
            'name': name,
            'purchase_date': purchase_date
        }
        stock_collection.insert_one(stock)

        return jsonify({'id': stock_id}), 201

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['GET'])
def get_stock(id):
    try:
        stock = stock_collection.find_one({'id': id})
        if stock:
            return jsonify(stock), 200
        return jsonify({'error': "Not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['PUT'])
def update_stock(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Malformed data"}), 400
        if not payload['id'] or payload['id'] != id:
            return jsonify({"error": "Malformed data"}), 400
        stock = stock_collection.find_one({'id': id})
        if not stock:
            return jsonify({"error": "Not found"}), 404

        required_fields = ['id', 'symbol', 'purchase_price', 'shares', 'name', 'purchase_date']
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"Malformed data: Missing {field}"}), 400
            stock[field] = payload[field]
        if '_id' in stock:
            del stock['_id']
        result = stock_collection.update_one({'id': id, }, {'$set': stock})
        if result.modified_count > 0:
            return jsonify({"id": stock['id']}), 200
        else:
            raise Exception
    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        result = stock_collection.delete_one({"id": id})
        if result.deleted_count == 0:
            return jsonify({'error': "Not found"}), 404
        return jsonify({''}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def validate_date(date_string):
    if date_string == 'NA':
        return True

    try:
        datetime.strptime(date_string, "%d-%m-%Y")
        return True
    except ValueError:
        return False
