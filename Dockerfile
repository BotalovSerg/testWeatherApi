FROM python:3.11-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir -e .

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}

# Открываем порт
EXPOSE 8000

# Запускаем приложение через uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]