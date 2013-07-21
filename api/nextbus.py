import urllib2
from lxml import etree

class NextBus:
	# See http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf
	
	lines = {"2": "6124",
			 "3": "6124",
			 "38": "6425",
			 "38L": "5818",
			 "47": "6808",
			 "49": "6808"}
	api_url = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=%s&s=%s"


	def __init__(self):
		pass
		
	def splice_xml(self, line, stop):
		three_times = (line, ["?","?","?"])
		data = urllib2.urlopen(self.api_url % (line, stop)).read()
		xml = etree.XML(data)
		try:
			three_times[1][0] = xml[0][0][0].attrib["minutes"]
		except:
			pass
		try:	
			three_times[1][1] = xml[0][0][1].attrib["minutes"]
		except:
			pass
		try:
			three_times[1][2] = xml[0][0][2].attrib["minutes"]
		except:
			pass
		return three_times

	def get_times(self, line="all"):
		times_list = []
		if line == "all":
			for l in self.lines:
				times_list.append(self.splice_xml(l, self.lines[l]))
		else:
			times_list.append(self.splice_xml(line, self.lines[line]))
		return times_list
