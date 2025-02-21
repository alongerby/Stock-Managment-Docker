import os
import signal
from datetime import datetime
import uuid
from flask import Blueprint, jsonify, request, current_app

stocks_bp = Blueprint('stocks', __name__)
TYPE_CASTS = {"shares": int, "purchase price": float}


@stocks_bp.route('/', methods=['GET'])
def get_stocks():
    try:
        stock_collection = stocks_bp.stock_collection
        query_params = request.args.to_dict()
        if not query_params:
            stocks = list(stock_collection.find({}, {"_id": 0}))
            return jsonify(stocks), 200

        filter_query = {}
        for field, value in query_params.items():
            if field in TYPE_CASTS:
                filter_query[field] = TYPE_CASTS[field](value)
            else:
                filter_query[field] = value

        # Query the database with the constructed filter
        filtered_stocks = list(stock_collection.find(filter_query, {"_id": 0}))

        return jsonify(filtered_stocks), 200

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/', methods=['POST'])
def create_stock():
    try:
        stock_collection = stocks_bp.stock_collection
        if request.content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415

        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Malformed data"}), 400

        required_fields = ['symbol', 'purchase price', 'shares']

        for field in required_fields:
            if field not in payload:
                return jsonify({"error": "Malformed data"}), 400

        if stock_collection.find_one({'symbol': payload['symbol']}):
            return jsonify({"error": "Malformed data"}), 400

        if not isinstance(payload['symbol'], str) or not isinstance(payload['purchase price'],
                                                                    (int, float)) or not isinstance(payload['shares'],
                                                                                                    int):
            return jsonify({"error": "Malformed data"}), 400

        stock_id = str(uuid.uuid4())
        name = payload.get('name', 'NA')
        purchase_date = payload.get('purchase date', 'NA')
        if not validate_date(purchase_date):
            return jsonify({"error": "Malformed data"}), 400

        stock = {
            '_id': stock_id,
            'id': stock_id,
            'symbol': payload['symbol'].upper(),
            'purchase price': round(payload['purchase price'], 2),
            'shares': payload['shares'],
            'name': name,
            'purchase date': purchase_date
        }
        stock_collection.insert_one(stock)

        return jsonify({'id': stock_id}), 201

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['GET'])
def get_stock(id):
    try:
        stock_collection = stocks_bp.stock_collection
        stock = stock_collection.find_one({'id': id}, {"_id": 0})
        if stock:
            return jsonify(stock), 200
        return jsonify({'error': "Not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['PUT'])
def update_stock(id):
    try:
        stock_collection = stocks_bp.stock_collection
        stock = stock_collection.find_one({'id': id}, {"_id": 0})
        if not stock:
            return jsonify({"error": "Not found"}), 404
        if request.content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Malformed data"}), 400
        if not payload.get('id') or payload.get('id') != id:
            return jsonify({"error": "Malformed data"}), 400

        required_fields = ['id', 'symbol', 'purchase price', 'shares', 'name', 'purchase date']
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": "Malformed data"}), 400
            stock[field] = payload[field]
        result = stock_collection.update_one({'id': id, }, {'$set': stock})
        return jsonify({"id": stock['id']}), 200

    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stocks_bp.route('/<string:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        stock_collection = stocks_bp.stock_collection
        result = stock_collection.delete_one({"id": id})
        if result.deleted_count == 0:
            return jsonify({'error': "Not found"}), 404
        return '', 204
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
