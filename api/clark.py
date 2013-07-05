from flask import Flask, make_response
import json
import time
from weather import Weather


app = Flask(__name__)


@app.route("/")
def dashboard():
    #  Time
    local_datetime = time.localtime()
    local_time = time.strftime("%H:%M:%S", local_datetime)
    local_date = time.strftime("%Y-%m-%d", local_datetime)

    #  Weather
    w = Weather()
    current_temperature = w.get_current_temperature()
    condition = w.get_current_condition()
    weather_image = 'img/%s.png' % condition.lower()

    data = {
        'time': local_time,
        'date': local_date,
        'weather': {
            'temperature_unit': w.temperature_unit,
            'today': {
                'temperature': w.get_current_temperature(),
                'low': w.get_today_low(),
                'high': w.get_today_high(),
                'high': current_temperature,
                'condition': condition,
                'image': weather_image,
            }
         }
    }

    res = make_response(json.dumps(data))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

if __name__ == "__main__":
    app.run(debug=True)
