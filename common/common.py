from flask import jsonify


def server_error_res(e):
    return jsonify({"server error": str(e)}), 500


def wrong_type_res():
    return jsonify({"error": "Expected application/json media type"}), 415


def not_found_res():
    return jsonify({'error': "Not found"}), 404


def malformed_res():
    return jsonify({"error": "Malformed data"}), 400