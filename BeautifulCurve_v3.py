from bs4 import BeautifulSoup
try:
	from urllib.request import urlopen
except Exception:
	from urllib import urlopen

import collections
from math import exp
from scipy.optimize import leastsq
from numpy import array, nditer

def nsEval(x,p):
	'''Given parameters and the x's, return NS yields'''
	
	nsOut=[]
	for i in nditer(x):
		nsOut.append(round(p[0] + p[1]*(1-exp(-i/p[3]))/(i/p[3])+p[2]*((1-exp(-i/p[3]))/(i/p[3])-exp(-i/p[3])),6))

	# Convert list to array
	nsArray = array(nsOut)*100
	return nsArray

def nsCurvFunc(p, y, x):
	'''
	p is the parameters in a tuple
	y is an array of yields
	x is an array of maturities

	Given the parameters, calculate Nelson-Siegel values for each 
	node on the curve and return the residual values in an array'''

	# Unpack parameter tuple
	a1, a2, a3, B = p

	# Iterate over the array and perform NS calculation
	nsOut = []
	for i in nditer(x):
		nsOut.append(round(a1 + a2*(1-exp(-i/B))/(i/B)+a3*((1-exp(-i/B))/(i/B)-exp(-i/B)),6))

	# Convert list to array
	nsArray = array(nsOut)*100
	
	# Find the errors for each node
	err = y - nsArray
	
	# print(p)
	# print(err)
	return err


def dictToList(CurveDict):
	'''Break dict into lists'''
	x=[]
	y=[]
	for k, v in CurveDict.items():
		x.append(round(float(v[0]),6))
		y.append(round(float(v[1]),6))

	return [y,x]


def nelsonSiegel(curve):
	''' Given the most recent curve, finds the parameters to 
	minimize the error of the Nelson-Siegel model.'''
	nsInit = array([.1,.1,.1,1.5])

	# Save the date, then drop it from the curve dict
	cDate = curve['current_date']
	curve.pop('current_date')

	curveLists = dictToList(curve)

	# Convert to array
	x_arr = array(curveLists[1])
	y_arr = array(curveLists[0])

	# Pass the arrays and initial parameter values to the solver
	plsq = leastsq(nsCurvFunc, nsInit, args=(y_arr, x_arr),full_output=0,epsfcn=0.00001)

	# Return only the parameters
	return plsq[0]

def getCurve():
	''' Retrieves the most recent curve from Treasury's website'''

	url = 'http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

	# Get the page
	page = urlopen(url)

	#Turn the page into soup
	soup = BeautifulSoup(page)

	# Narrow page down to just the curves
	s = soup.find_all("td", class_="text_view_data")

	# Turn the Soup of curves into an ordered dict
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
	print('NS Params: ',nsParams)

	# Get the list of maturities and yields from output dict
	xList = array(dictToList(c))

	# These are the current market yields
	print('Observed Yields: ')
	for n in xList[0]:
		print(n)
	
	# Use nsEval to generate the NS values given the model parameters
	print('NS Output: ')
	
	# nsY = nsEval(xList[1],nsParams)
	for o in nsEval(xList[1],nsParams):
		print(o)

if __name__ == '__main__':
	main()