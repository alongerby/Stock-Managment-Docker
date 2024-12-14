from flask import Blueprint, jsonify, request

stock_bp = Blueprint('stock', __name__)


@stock_bp.route('/<string:id>', methods=['GET'])
def get_stock(id):
    try:
        for stock in stockDB:
            if stock['id'] == id:
                return jsonify(stock), 200
        return jsonify({'error': "Not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stock_bp.route('/<string:id>', methods=['PUT'])
def update_stock(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Malformed data"}), 400
        if not payload['id'] or payload['id'] != id:
            return jsonify({"error": "Malformed data"}), 400
        stock = next((s for s in stockDB if s['id'] == id), None)
        if not stock:
            return jsonify({"error": "Not found"}), 404

        required_fields = ['id', 'symbol', 'purchase_price', 'shares', 'name', 'purchase_date']
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"Malformed data: Missing {field}"}), 400
            stock[field] = payload[field]
        return jsonify({"id": stock['id']}), 200
    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@stock_bp.route('/<string:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        for stock in stockDB:
            if stock['id'] == id:
                stockDB.remove(stock)
                return jsonify({''}), 204
        return jsonify({'error': "Not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
