# Weather Forecast Web App

Это веб-приложение, позволяющее пользователю вводить название города и получать прогноз погоды с помощью [Open-Meteo API](https://open-meteo.com/).

## ✅ Возможности:

- Поиск погоды по названию города.
- Автодополнение при вводе.
- Хранение истории посещённых городов.
- API `/stats` показывает количество посещений каждого города.
- Тесты покрывают основные функции.
- Все это работает внутри Docker-контейнера.

## 🛠️ Технологии:

- Python + Flask
- Open-Meteo API
- SQLite
- Sqlalchemy
- JavaScript + HTML/CSS
- Docker
- unittest

## 🚀 Как запустить:

### Локально:

```bash
uv sync
flask run 
or
gunicorn main:app
```
