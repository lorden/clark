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

    data = {
        'time': local_time,
        'date': local_date,
        'weather': {
            'temperature_unit': w.temperature_unit,
            'today': {
                'temperature': w.get('today.temperature'),
                'low': w.get('today.low'),
                'high': w.get('today.high'),
                'condition': w.get('today.condition'),
                'image': 'img/%s.png' % w.get('today.condition').lower().replace(' ', '_'),
            },
            'tomorrow': {
                'low': w.get('tomorrow.low'),
                'high': w.get('tomorrow.high'),
                'condition': w.get('tomorrow.condition'),
                'image': 'img/%s.png' % w.get('tomorrow.condition').lower().replace(' ', '_'),
            },
            'after_tomorrow': {
                'low': w.get('after_tomorrow.low'),
                'high': w.get('after_tomorrow.high'),
                'condition': w.get('after_tomorrow.condition'),
                'image': 'img/%s.png' % w.get('after_tomorrow.condition').lower().replace(' ', '_'),
            }
         }
    }

    print
    print data
    print
        
    res = make_response(json.dumps(data))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

if __name__ == "__main__":
    app.run(debug=True)
