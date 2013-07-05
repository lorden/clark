from werkzeug.contrib.cache import MemcachedCache
import urllib2
import json
from lxml import etree

class Weather:
    
    api_appid = 'c18d38cad3eca59f418c551f45f32ff1'
    cache = None
    latitude = 0
    longitude = 0
    api_url = 'http://weather.yahooapis.com/forecastrss?w=12797160&u=c'
    temperature_unit = 'C'
    values = {
        'today': {}, 
        'tomorrow': {}, 
        'after_tomorrow': {}
    }

    def __init__(self, unit='metric'):
        self.cache = MemcachedCache(['127.0.0.1:11211'])
        if unit == 'imperial':
            self.temperature_unit = 'F'
        self.parse_data(self.get_data())

    def get_data(self):
        wdata = self.cache.get('weather-data')
        if wdata is None:
            print "Cache is empty"
            print "Querying: %s" % self.api_url
            wdata = urllib2.urlopen(self.api_url).read()
            print "Response: %s" % wdata
            self.cache.set('weather-data', wdata, timeout=10 * 60)
        return wdata


    def parse_data(self, data):
        namespaces = { 'yweather': 'http://xml.weather.yahoo.com/ns/rss/1.0' }
        data = etree.XML(data)
        # Current temperature
        self.values['today']['temperature'] = data.xpath(
            '//channel/item/yweather:condition', 
            namespaces=namespaces)[0].attrib['temp']
        # Today's values
        self.values['today']['condition'] = data.xpath(
            '//channel/item/yweather:condition', 
            namespaces=namespaces)[0].attrib['text']
        self.values['today']['low'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[0].attrib['low']
        self.values['today']['high'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[0].attrib['high']
        # Tomorrow's values
        self.values['tomorrow']['condition'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[1].attrib['text']
        self.values['tomorrow']['low'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[1].attrib['low']
        self.values['tomorrow']['high'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[1].attrib['high']
        # After tomorrow's low and high
        self.values['after_tomorrow']['condition'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[2].attrib['text']
        self.values['after_tomorrow']['low'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[2].attrib['low']
        self.values['after_tomorrow']['high'] = data.xpath(
            '//channel/item/yweather:forecast', 
            namespaces=namespaces)[2].attrib['high']

    def get(self, string):
        keys = string.split('.')
        value = self.values
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None
        return value
            
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
