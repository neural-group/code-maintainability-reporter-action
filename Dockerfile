FROM python:3.12-slim

RUN pip install uv

WORKDIR /app
COPY requirements.lock ./
COPY src ./
COPY entrypoint.sh ./

RUN uv pip install --no-cache --system -r requirements.lock

ENTRYPOINT ["./entrypoint.sh"]
