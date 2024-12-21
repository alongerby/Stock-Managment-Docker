FROM python:alpine3.17

WORKDIR /app

COPY /common /app

COPY ./capital_gains_service /app

COPY capital_gains_service/src/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV API_KEY=//nNbI2cdJwkKK80mdi/lA==dJjJ97of2WZcAngR

ENV PYTHONPATH=/app

ENV URI=mongodb+srv://alongerby007:Z2-t-rg2i2jhfF7@portfolio.3d14i.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio

CMD ["python", "src/app.py"]