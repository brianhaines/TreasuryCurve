import requests
import xml.etree.ElementTree as ET

"""
The virtual environment for this project is xmlEnv
"""

class curveGet():
	data = requests.get('http://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yield')
	xml = ET.fromstring(data.content)
	 #The .// below is syntax particular to ET
	entries = xml.findall('.//{http://www.w3.org/2005/Atom}entry')
	
	def __init__(self):
		#This collects all of the entries into a list called curveList
		self.curveList = []
		for entry in self.entries:
			self.curveList.append(self.elementsToDict(entry))


		self.id = 	self.rateGet('id')
		self.date = 	self.rateGet('NEW_DATE')
		self.month1 = 	self.rateGet('BC_1MONTH')
		self.month3 = 	self.rateGet('BC_3MONTH')
		self.month6 = 	self.rateGet('BC_6MONTH')
		self.year1 = 	self.rateGet('BC_1YEAR')
		self.year2 = 	self.rateGet('BC_2YEAR')
		self.year3 = 	self.rateGet('BC_3YEAR')
		self.year5 = 	self.rateGet('BC_5YEAR')
		self.year7 = 	self.rateGet('BC_7YEAR')
		self.year10 = 	self.rateGet('BC_10YEAR')
		self.year20 = 	self.rateGet('BC_20YEAR')
		self.year30 = 	self.rateGet('BC_30YEAR')

	def getTagName(self, element):
		"""
		Cleans up the Tag, makes them easier to read
		"""
		return element.tag.rsplit('}')[1]

	def elementsToDict(self, entry):
		"""Given an ElementTree representation for an 'element' node,
		construct a corresponding Python dictionary
		"""
		d = {}

		idTagRaw = entry.find('{http://www.w3.org/2005/Atom}id').text
		idTagFinal = idTagRaw.split('(')[1].split(')')[0]

		d['id'] = idTagFinal
		for property in entry.find('{http://www.w3.org/2005/Atom}content/'):
			tagName = self.getTagName(property)
			d[tagName] = property.text
		return d


	def findLastEntry(self, entryList):
		"""
		Given a list of entries, find the one with the larges 'id' value.
		This entry will be the most recent published on the website
		"""
		i = 0
		for t in entryList:
			if i == 0:
				idVal = (t['id'])
				i += 1
			elif i > 0:
				if t['id'] > idVal:
					idVal = t['id']
					#print(i)
					i += 1
		return i-1

	def rateGet(self, node):
		"""
		This will take a tag/dict key and return the associated value
		"""		
		return node, self.curveList[self.findLastEntry(self.curveList)][node]