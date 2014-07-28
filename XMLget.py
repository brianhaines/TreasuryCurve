
import requests
import xml.etree.ElementTree as ET

"""
The virtual environment for this project is xmlEnv
"""

data = requests.get('http://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yield')
xml = ET.fromstring(data.content)

 #The .// below is syntax particular to ET
entries = xml.findall('.//{http://www.w3.org/2005/Atom}entry')

def getTagName(element):
	"""
	Cleans up the Tag, makes them easier to read
	"""
	return element.tag.rsplit('}')[1]

def elementsToDict(entry):
	"""Given an ElementTree representation for an 'element' node,
	construct a corresponding Python dictionary
	"""
	d = {}

	idTagRaw = entry.find('{http://www.w3.org/2005/Atom}id').text
	idTagFinal = idTagRaw.split('(')[1].split(')')[0]

	d['id'] = idTagFinal
	for property in entry.find('{http://www.w3.org/2005/Atom}content/'):
		tagName = getTagName(property)
		d[tagName] = property.text
	return d


def findLastEntry(entryList):
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

def rateGet(node, nodeList):
	"""
	This will take a tag/dict key and return the associated value
	"""
	return node, nodeList[findLastEntry(nodeList)][node]

#This collects all of the entries into a list
curveList = []
for entry in entries:
	curveList.append(elementsToDict(entry))
print(curveList[len(curveList)-1]) 

print(rateGet('BC_10YEAR',curveList))