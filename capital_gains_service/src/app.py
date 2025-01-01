from flask import Flask
from resources.capital_gains import capital_gains_bp
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
app = Flask(__name__)

uri = "mongodb://mongodb:27017"

app.register_blueprint(capital_gains_bp, url_prefix='/capital-gains')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["portfolio"]
app.config["DB"] = db
capital_gains_bp.stock1_collection = db["stocks1"]
capital_gains_bp.stock2_collection = db["stocks2"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

