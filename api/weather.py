from werkzeug.contrib.cache import MemcachedCache
import urllib2
import json


class Weather:
    
    api_appid = 'c18d38cad3eca59f418c551f45f32ff1'
    cache = None
    latitude = 0
    longitude = 0
    api_url = ''
    temperature_unit = 'C'

    def __init__(self, unit='metric'):
        self.cache = MemcachedCache(['127.0.0.1:11211'])
        self.latitude = 37.786282
        self.longitude = -122.423937
        self.api_url = 'http://api.openweathermap.org/data/2.5/weather' +\
                       '?lat=%s&lon=%s&cnt=3' % (
                        self.latitude, self.longitude)
        if unit == 'imperial':
            self.temperature_unit = 'F'

    def get_data(self):
        wdata = self.cache.get('weather-data')
        wdata = None
        if wdata is None:
            print "Cache is empty"
            print "Querying: %s" % self.api_url
            wdata = json.loads(urllib2.urlopen(self.api_url).read())
            print "Response: %s" % wdata
            self.cache.set('weather-data', wdata, timeout=10 * 60)
        return wdata

    def get_current_temperature(self):
        data = self.get_data()
        print "dump: %s" % json.dumps(data)
        print data['main']
        return self.convert(data['main']['temp'], 'K', self.temperature_unit)

    def convert(self, value, from_unit, to_unit):
        if from_unit == 'K' and to_unit == 'C':
            return float(value) - 273.15
        elif from_unit == 'K' and to_unit == 'F':
            return (float(value) * 5 / 9) - 459.67

    def get_description(self):
        data = self.get_data()
        filename = data['weather'][0]['description'].replace(' ', '_').lower()
        if data['dt'] >= data['sys']['sunrise'] and \
                data['dt'] <= data['sys']['sunset']:
            return "%s_day" % filename
        else:
            return "%s_night" % filename
