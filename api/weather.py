from werkzeug.contrib.cache import MemcachedCache
import urllib2
import json


weather_api_appid = 'c18d38cad3eca59f418c551f45f32ff1'
cache = MemcachedCache(['127.0.0.1:11211'])


def get_data(units="metric"):
    weather_url = 'http://api.openweathermap.org/data/2.5/' +\
                  'weather?q=San%20Francisco,%20US'
    wdata = cache.get('weather-data')
    if wdata is None:
        print 'Retrieving'
        if units == 'imperial':
            weather_url = "%s&units=imperial" % weather_url
        else:
            weather_url = "%s&units=metric" % weather_url

        weather_data = urllib2.urlopen(weather_url).read()
        wdata = cache.set('weather-data', weather_data, timeout=10 * 60)
    return json.loads(wdata)


def get_current_temperature(units):
    data = get_data(units)
    return data['main']['temp']


def get_temperature_unit(units):
    return 'F' if units == 'imperial' else 'C'


def get_description():
    data = get_data()
    filename = data['weather'][0]['description'].replace(' ', '_').lower()
    if data['dt'] >= data['sys']['sunrise'] and \
            data['dt'] <= data['sys']['sunset']:
        return "%s_day" % filename
    else:
        return "%s_night" % filename
