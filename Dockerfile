FROM python:3.13.3-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --prefix "/opt/venv"

FROM python:3.13.3-slim

WORKDIR /app

COPY --from=builder /opt/venv /usr/local

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--workers", "3", "--bind", "0.0.0.0:8000"]