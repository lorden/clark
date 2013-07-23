from flask import Flask, make_response
import json
import time
from weather import Weather
from Calendar import Calendar
from nextbus import NextBus


app = Flask(__name__)

@app.route("/bus")
def bus():
    n = NextBus()
    data = n.get_times()
    res = make_response(json.dumps(data))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/calendar")
def calendar():
    from hashlib import md5
    #  Calendar
    cal = Calendar()
    with open('calendars.cfg') as f:
        c = f.readline()
        events = []
        while c:
            cid, cname = c.split(',')
            events += cal.get_events(cid.strip(), cname.strip())
            c = f.readline()
    # Remove duplicates, only for 2 cals
    single_events = {}
    for e in events:
        key = ''
        if e['name']:
            key += e['name'].encode('ascii', 'ignore')
        if e['start']:
            key += e['start'].encode('ascii', 'ignore')
        key = md5(key).hexdigest()
        if key not in single_events:
            single_events[key] = e
        else:
            single_events[key]['calendar'] = 'all'
    
    events = sorted(single_events.values(), key=lambda event: event['start'])
    data = { 'events': events }

    res = make_response(json.dumps(data))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

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

        
    res = make_response(json.dumps(data))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

if __name__ == "__main__":
    app.run(debug=True)
