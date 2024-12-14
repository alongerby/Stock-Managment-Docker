from flask import Flask
from resources.stock_value import stock_value_bp
from resources.stocks import stocks_bp
from resources.portfolio_value import portfolio_value_bp

app = Flask(__name__)

app.register_blueprint(stock_value_bp, url_prefix='/stock-value')
app.register_blueprint(stocks_bp, url_prefix='/stocks')
app.register_blueprint(portfolio_value_bp, url_prefix='/portfolio-value')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

