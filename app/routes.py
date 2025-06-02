from flask import (
    Blueprint,
    Response,
    jsonify,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    make_response,
)
from app import logger
from app.api import get_weather
from app.database.config_db import db_session, get_db
from app.database.request_db import (
    get_all_search_stats,
    get_or_create_city,
    update_or_create_search_history,
    get_cities_by_prefix,
)
from app.utils import validate_city, InvalidCityError

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index() -> Response | str:
    """
    Главная страница с формой поиска погоды.

    GET: Отображает форму поиска
    POST: Обрабатывает отправку формы и перенаправляет на страницу погоды

    Возвращает:
        - При GET: HTML страницу с формой
        - При POST: Перенаправление на страницу погоды или обратно на форму с ошибкой
    """
    if request.method == "POST":
        try:
            city = validate_city(request.form.get("city"))

            city_entry = get_or_create_city(db_session, city)
            update_or_create_search_history(db_session, city_entry.id)

            response = make_response(redirect(url_for("main.show_weather", city=city)))
            response.set_cookie(
                "last_city",
                city,
                max_age=10,
                secure=True,
                httponly=True,
                samesite="Lax",
            )
            return response
        except InvalidCityError as e:
            flash(str(e))
            return redirect(url_for("main.index"))

    last_city = request.cookies.get("last_city")
    return render_template("index.html", last_city=last_city)


@bp.route("/weather/<city>")
def show_weather(city) -> Response | str:
    """
    Страница с отображением погоды для указанного города.

    Параметры:
        city (str): Название города

    Возвращает:
        - HTML страницу с погодой или перенаправление на главную с ошибкой
    """
    weather_data = get_weather(city)
    if not weather_data:
        flash("Не удалось получить данные о погоде для этого города.")
        return redirect(url_for("main.index"))

    response = render_template("weather.html", weather=weather_data)
    return response


@bp.route("/api/cities")
def cities() -> Response:
    """
    API endpoint для получения статистики поиска городов.

    Возвращает:
        - JSON с массивом объектов статистики:
          {
            "city": str,
            "count": int,
            "last_visited": str (ISO format)
          }
    """
    stats = get_all_search_stats(db_session)
    result = [
        {
            "city": name,
            "count": count,
            "last_visited": last_visited.isoformat(),
        }
        for name, count, last_visited in stats
    ]
    return jsonify(result)


@bp.route("/api/autocomplete")
def autocomplete() -> Response:
    """
    Обработчик автозаполнения городов.

    Параметры:
    - q: строка поиска (минимум 2 символа)

    Возвращает:
    - JSON-массив с подходящими городами (максимум 10)
    - 400 если запрос слишком короткий
    - 500 при ошибке сервера
    """
    try:
        q = request.args.get("q", "").strip()

        if len(q) < 2:
            return jsonify({"error": "Строка поиска должна содержать минимум 2 символа"}), 400

        db = next(get_db())

        try:
            cities = get_cities_by_prefix(db, q, limit=10)
            return jsonify(cities)
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Ошибка в автозаполнении: {str(e)}")
        return jsonify({"error": "Произошла ошибка при поиске городов"}), 500
