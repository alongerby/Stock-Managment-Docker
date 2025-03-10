FROM python:alpine3.17

WORKDIR ./app

COPY . /app

COPY src/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV API_KEY=//nNbI2cdJwkKK80mdi/lA==dJjJ97of2WZcAngR

CMD ["python", "src/app.py"]
