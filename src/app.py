import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_weather(city: str) -> str:
    """
    Fetches current temperature (in Celsius) for given city.
    Raises:
      - RuntimeError if OPENWEATHER_API_KEY is missing.
      - ValueError if the city isn’t found.
    """
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(f"City '{city}' not found")
    kelvin = resp.json()["main"]["temp"]
    celsius = round(kelvin - 273.15)
    return f"{celsius} Celsius"

@app.route("/weather")
def weather():
    city = request.args.get("city")
    if not city:
        return jsonify(error="City parameter is required"), 400
    try:
        temperature = get_weather(city)
        return jsonify(temperature=temperature)
    except ValueError as ve:
        return jsonify(error=str(ve)), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
