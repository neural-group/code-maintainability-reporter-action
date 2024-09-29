FROM nikolaik/python-nodejs:python3.12-nodejs22-slim

WORKDIR /app
COPY requirements.lock ./
COPY src ./
COPY entrypoint.sh ./

RUN uv pip install --no-cache --system -r requirements.lock

ENTRYPOINT ["./entrypoint.sh"]
