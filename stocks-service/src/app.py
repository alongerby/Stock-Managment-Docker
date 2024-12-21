import logging

from flask import Flask
from resources.stock_value import stock_value_bp
from resources.stocks import stocks_bp
from resources.portfolio_value import portfolio_value_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()
uri = "mongodb://mongodb:27017"
collection = os.getenv('COLLECTION')
API_KEY = os.getenv('API_KEY')

app.register_blueprint(stock_value_bp, url_prefix='/stock-value')
app.register_blueprint(stocks_bp, url_prefix='/stocks')
app.register_blueprint(portfolio_value_bp, url_prefix='/portfolio-value')

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["portfolio"]
portfolio_value_bp.stock_collection = db[collection]
portfolio_value_bp.API = API_KEY
stock_value_bp.API = API_KEY
stock_value_bp.stock_collection = db[collection]
stocks_bp.stock_collection = db[collection]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

