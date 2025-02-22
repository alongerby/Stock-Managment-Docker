import requests
import pytest

stock1_id_global = None
stock2_id_global = None
stock3_id_global = None
stocks_url = "http://localhost:5001/stocks"
stock_value_url = "http://localhost:5001/stock-value"
portfolio_value_url = "http://localhost:5001/portfolio-value"

def test_post_three_stocks():
    global stock1_id_global
    global stock2_id_global
    global stock3_id_global

    # Define payloads for stock1, stock2, and stock3
    stock1 = {
        "name": "NVIDIA Corporation",
        "symbol": "NVDA",
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    }
    stock2 = {
        "name": "Apple Inc.",
        "symbol": "AAPL",
        "purchase price": 183.63,
        "purchase date": "22-02-2024",
        "shares": 19
    }
    stock3 = {
        "name": "Alphabet Inc.",
        "symbol": "GOOG",
        "purchase price": 140.12,
        "purchase date": "24-10-2024",
        "shares": 14
    }

    # Issue three POST requests
    response1 = requests.post(stocks_url, json=stock1)
    response2 = requests.post(stocks_url, json=stock2)
    response3 = requests.post(stocks_url, json=stock3)

    # Assert that each request returns a status code of 201
    assert response1.status_code == 201, f"Expected status 201 for stock1 but got {response1.status_code}"
    assert response2.status_code == 201, f"Expected status 201 for stock2 but got {response2.status_code}"
    assert response3.status_code == 201, f"Expected status 201 for stock3 but got {response3.status_code}"

    # Parse JSON responses to extract the IDs
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()

    # Assert that the 'id' field is present in each response
    assert "id" in data1, "Response for stock1 does not contain an 'id' field"
    assert "id" in data2, "Response for stock2 does not contain an 'id' field"
    assert "id" in data3, "Response for stock3 does not contain an 'id' field"

    id1 = data1["id"]
    id2 = data2["id"]
    id3 = data3["id"]

    # Assert that all three IDs are unique
    assert id1 != id2 and id1 != id3 and id2 != id3, "The returned IDs are not unique"

    stock1_id_global = id1
    stock2_id_global = id2
    stock3_id_global = id3


def test_get_with_id():
    global stock1_id_global
    response = requests.get(f"{stocks_url}/{stock1_id_global}")

    assert response.status_code == 200, f"Expected status 200 for stock1 but got {response.status_code}"

    data = response.json()
    assert data.get("symbol", "") == "NVDA", "Response for stock1 does not contain NVDA symbol"


def test_get_stocks():
    response = requests.get(stocks_url)

    assert response == 200, f"Expected status 200 for get stocks but got {response.status_code}"
    data = response.json()

    assert len(data) == 3, f"Expected 3 embedded JSON objects, but got {len(data)}"


def test_stock_value():
    global stock1_id_global, stock2_id_global, stock3_id_global

    # Execute GET /stock-value/{ID} for each stock
    response1 = requests.get(f"{stock_value_url}/{stock1_id_global}")
    response2 = requests.get(f"{stock_value_url}/{stock2_id_global}")
    response3 = requests.get(f"{stock_value_url}/{stock3_id_global}")

    # Assert that each request returns a status code of 200
    assert response1.status_code == 200, f"Expected status 200 for stock1 value but got {response1.status_code}"
    assert response2.status_code == 200, f"Expected status 200 for stock2 value but got {response2.status_code}"
    assert response3.status_code == 200, f"Expected status 200 for stock3 value but got {response3.status_code}"

    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()

    # Validate the symbol for each stock value response
    assert data1.get("symbol", "") == "NVDA", f"Expected symbol 'NVDA' but got {data1.get('symbol')}"
    assert data2.get("symbol", "") == "AAPL", f"Expected symbol 'AAPL' but got {data2.get('symbol')}"
    assert data3.get("symbol", "") == "GOOG", f"Expected symbol 'GOOG' but got {data3.get('symbol')}"


def test_portfolio_value():
    global stock1_id_global, stock2_id_global, stock3_id_global

    # Get individual stock values
    response1 = requests.get(f"{stock_value_url}/{stock1_id_global}")
    response2 = requests.get(f"{stock_value_url}/{stock2_id_global}")
    response3 = requests.get(f"{stock_value_url}/{stock3_id_global}")

    assert response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200, "One of the stock value requests failed."

    sv1 = response1.json().get("stock value", 0)
    sv2 = response2.json().get("stock value", 0)
    sv3 = response3.json().get("stock value", 0)

    total_stock_value = sv1 + sv2 + sv3

    # Execute GET /portfolio-value
    response_portfolio = requests.get(portfolio_value_url)
    assert response_portfolio.status_code == 200, f"Expected status 200 for portfolio value but got {response_portfolio.status_code}"

    pv = response_portfolio.json().get("portfolio value", 0)
    # Allow a tolerance of ±3% (i.e., between 97% and 103% of pv)
    lower_bound = pv * 0.97
    upper_bound = pv * 1.03

    assert lower_bound <= total_stock_value <= upper_bound, (
        f"Sum of stock values {total_stock_value} is not within ±3% of portfolio value {pv}"
    )


def test_post_stock7_missing_symbol():
    # stock7 missing the required "symbol" field
    stock7 = {
        "name": "Amazon.com, Inc.",
        "purchase price": 134.66,
        "purchase date": "18-06-2024",
        "shares": 7
    }
    response = requests.post(stocks_url, json=stock7)
    assert response.status_code == 400, f"Expected status 400 for stock7 missing symbol but got {response.status_code}"


def test_delete_stock2():
    global stock2_id_global
    # Execute DELETE /stocks/{ID} for stock2 (Apple Inc.)
    response = requests.delete(f"{stocks_url}/{stock2_id_global}")
    assert response.status_code == 204, f"Expected status 204 for DELETE stock2 but got {response.status_code}"


def test_get_deleted_stock2():
    global stock2_id_global
    # After deletion, a GET request for stock2 should return 404
    response = requests.get(f"{stocks_url}/{stock2_id_global}")
    assert response.status_code == 404, f"Expected status 404 for deleted stock2 but got {response.status_code}"


def test_post_stock8_incorrect_date():
    # stock8 with an incorrect purchase date format
    stock8 = {
        "name": "Amazon.com, Inc.",
        "symbol": "AMZN",
        "purchase price": 134.66,
        "purchase date": "Tuesday, June 18, 2024",  # Incorrect format; should be DD-MM-YYYY
        "shares": 7
    }
    response = requests.post(stocks_url, json=stock8)
    assert response.status_code == 400, f"Expected status 400 for stock8 with incorrect purchase date but got {response.status_code}"



