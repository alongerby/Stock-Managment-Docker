FROM python:alpine3.17

WORKDIR /app

COPY /common /app

COPY ./capital_gains_service /app

COPY capital_gains_service/src/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV API_KEY=//nNbI2cdJwkKK80mdi/lA==dJjJ97of2WZcAngR

ENV PYTHONPATH=/app

CMD ["python", "src/app.py"]