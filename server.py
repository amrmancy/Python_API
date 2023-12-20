# this file could be called also main.py or server.py

from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)  # that makes our app a flask app

# defining routes


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def get_weather():
    city = request.args.get(
        "city"
    )  # This line retrieves the value of the "city" parameter from the query string of the URL. For example, if the URL is "/weather?city=Berlin", this line will extract "Berlin" as the value of the city variable.
    
    
    #check for empty strings or string with only spaces
    if not bool(city.strip()):
        city="cairo"
        
    weather_data = get_current_weather(city)
    #city is not found by API
    if  weather_data['cod'] != 200:
        return render_template ('city-not-found.html')
    return render_template(  # sends params with the template
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
