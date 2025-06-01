from app import app
from app.api import get_weather


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/get")
def get_weather_api():
    print(get_weather("Екатеринбург"))
    return "Tets"
