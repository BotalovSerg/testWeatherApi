# Weather Forecast Web App

Это веб-приложение, позволяющее пользователю вводить название города и получать прогноз погоды с помощью [Open-Meteo API](https://open-meteo.com/).

## ✅ Возможности:

- Поиск погоды по названию города.
- Автодополнение при вводе (через собственную базу).
- Хранение истории посещённых городов.
- Отображение последнего запрошенного города через куки.
- API для получения статистики запросов: сколько раз какой город искали.
- Полностью рабочее приложение внутри Docker-контейнера.

## 🛠️ Технологии:

- Python + Flask
- Open-Meteo API (для данных о погоде)
- SQLAlchemy + SQLite (для хранения истории)
- JavaScript + HTML/CSS (фронтенд)
- Docker (для контейнеризации)

## 🌐 Доступные эндпоинты:

- GET / Отображает форму для ввода названия города.
- POST / Обработка формы поиска. Принимает название города, проверяет его, сохраняет историю посещений и перенаправляет на страницу с погодой.
- GET /weather/<city> Показывает прогноз погоды для указанного города.
- GET /api/cities Возвращает JSON со статистикой: сколько раз какой город искали и когда в последний раз.
- GET /api/autocomplete?q=<query> Возвращает JSON-массив подходящих названий городов на основе введённой строки.

## 🚀 Как запустить:

### Локально:
```bash
uv sync         # или pip install -r requirements.txt
flask run       # или gunicorn main:app
```
### Через Docker:
```bash
docker compose up --build -d
```
### Открыть в браузере:
👉 http://localhost:8000