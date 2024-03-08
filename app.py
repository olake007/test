from flask import Flask, render_template, request
import requests
from datetime import datetime
from matplotlib import pyplot as plt

app = Flask(__name__)

print('Hello World!')

x_time = [0,1,2,3,4,5,6]
y_temp = [18,15,13,9,8,8,11]
plt.plot(x_time, y_temp)
plt.savefig('test_chart')

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/result', methods=["GET", "POST"])
def result():
    api_key = "aa9496e9adb3bf2f85fa97e59f3b278a"
    form_city = request.form.get("city")
    form_lat = request.form.get("latitude")
    form_lon = request.form.get("longitude")
    print(form_lat)
    print(form_lon)
    if not form_city:
        url = ("http://api.openweathermap.org/data/2.5/weather?lat="
               + form_lat + "&lon=" + form_lon + "&APPID=" + api_key)

    else:
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + form_city + "&APPID=" + api_key

    print(url)

    response = requests.get(url).json()

    print(response)

    weather_list = response.get("weather", [{}])
    weather_one = weather_list[0]
    location = response.get("name")
    time_zone = response.get("timezone")
    time_stamp = response.get("dt")
    print(time_stamp)
    dt = datetime.fromtimestamp(time_stamp)
    print(dt)
    description = weather_one.get('weather', [0])
    temp_k = response.get("main", {}).get("temp")
    temp_c = int(temp_k) - 273.15
    wind_speed = response.get("wind").get("speed")

    weather_dict = {
        "location": location,
        "time_zone": time_zone,
        "time_stamp": time_stamp,
        "date_and_time": dt,
        "description": description,
        "temp_k": temp_k,
        "temp_c": temp_c,
        "wind_speed": wind_speed
    }

    return render_template('result.html', response=response, weather_dict=weather_dict)


if __name__ == '__main__':
    app.run(debug=True)
