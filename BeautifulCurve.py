from bs4 import BeautifulSoup
try:
	from urllib.request import urlopen
except Exception:
	from urllib import urlopen

import collections
from math import exp
import math


def nsFunc(m,a1,a2,a3,B):
	'''Given the inputs, returns the curve value estimated
	by the Nelson-Siegel model.'''
	nsOut = a1 + a2*(1-math.exp(-m/B))/(m/B)+a3*((1-math.exp(-m/B))/(m/B)-math.exp(-m/B)) 
	return round(nsOut*100,7)

def nsCurvFunc(curve, nsInit):
	'''Given the parameters, calculate Nelson-Siegel values for each 
	node on the curve'''
	nsErrTot=0
	for k,v in curve.items():
		nsVal = nsFunc(float(v[0]),*nsInit)
		nsErr = round((float(v[1]) - nsFunc(float(v[0]),*nsInit))**2,6)
		nsErrTot += nsErr
		curve[k] =curve[k] + (nsVal,nsErr)
	nsSolver(curve,nsInit)
	# Return squared errors
	return nsErrTot

def nsSolver(curve, nsInit):
	'''This function will take in initial values of the
	NS model, and find the values that minimize the squared error.
	1. Take initial parameters and adjust them up and down, capturing the 
	direction of the change in the error
	2. Move each parameter in it's error minimization direction.
	3. Other magic
	'''
	a1,a2,a3,B = nsInit
	


def nelsonSiegel(curve):
	''' Given the most recent curve, finds the parameters to 
	minimize the error of the Nelson-Siegel model.'''
	nsInit = (.036686,-.036184,-.042101,1.425282)
	# nsInit = (.036686,-.036184*.99,-.042101,1.425282)	
	# Save the date, then drop it from the curve dict
	cDate = curve['current_date']
	curve.pop('current_date')

	# Run the curve thr
	nsCurve = nsCurvFunc(curve, nsInit)
	print(nsCurve)

	# for k, v in nsCurve.items():
	# 	print(k , v)	

	# for k, v in nsCurve.items():
	# 	nsErr = round(float(v[1]) - nsFunc(float(v[0]),*nsInit),6)
	# 	print('In: ',v[0],v[1],' Out: ',nsFunc(float(v[0]),*nsInit),'Error: ',nsErr)

def getCurve():
	''' Retrieves the most recent curve from Treasury's website'''
	# url = 'http://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yield'
	url = 'http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

	page = urlopen(url)

	#Turn the page into soup
	soup = BeautifulSoup(page)

	s = soup.find_all("td", class_="text_view_data")

	w=collections.OrderedDict()
	w['Current_DATE'.lower()] = s[(len(s)-1)-11].contents[0]
	w['1MONTH'.lower()] = (.08333,s[(len(s)-1)-10].contents[0])
	w['3MONTH'.lower()] = (.25, s[(len(s)-1)-9].contents[0])
	w['6MONTH'.lower()] = (.5, s[(len(s)-1)-8].contents[0])
	w['1YEAR'.lower()] = (1 , s[(len(s)-1)-7].contents[0])
	w['2YEAR'.lower()] = (2, s[(len(s)-1)-6].contents[0])
	w['3YEAR'.lower()] = (3 , s[(len(s)-1)-5].contents[0])
	w['5YEAR'.lower()] = (5 , s[(len(s)-1)-4].contents[0])
	w['7YEAR'.lower()] = (7 , s[(len(s)-1)-3].contents[0])
	w['10YEAR'.lower()] = (10 , s[(len(s)-1)-2].contents[0])
	w['20YEAR'.lower()] = (20 , s[(len(s)-1)-1].contents[0])
	w['30YEAR'.lower()] = (30 , s[(len(s)-1)-0].contents[0])

	return w

def main():
	# Get the current curve
	c = getCurve()

	# Solve the Nelson-Siegel parameters
	nsParams = nelsonSiegel(c)

	# Use the parameters to solve for a specific date
	# return nsFunc(nsParams)

if __name__ == '__main__':
	main()