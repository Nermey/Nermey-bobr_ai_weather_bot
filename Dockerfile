FROM python:3.12

WORKDIR /bot

COPY bot/requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_KEY=$API_KEY
ENV BOT_TOKEN=$BOT_TOKEN

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /bot ./


CMD ["python", "main.py"]

