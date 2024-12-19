from flask import Flask
from resources.capital_gains import capital_gains_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()
uri = os.getenv('URI')
collection = os.getenv('COLLECTION')
API_KEY = os.getenv('API_KEY')

app.register_blueprint(capital_gains_bp, url_prefix='/capital-gains')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["portfolio"]
app.config["DB"] = db
capital_gains_bp.stock1_collection = db["stock1"]
capital_gains_bp.stock2_collection = db["stock2"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

