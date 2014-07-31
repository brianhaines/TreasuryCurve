"""
This will create a DB if one does not already exist, then populate it with all of the
yield curve data from XMLgetClass variable .curveList[]

Previous files are merged into one that uses functions to perform the various actions

When this file is run, it will:
1. Scrape yield curve info off the treasury.gov website 
2. Open a connection to a local db using sqlite3
3. Add any new curves to the database
4. Offer a means of extracting a specific curve term or all of them
"""

import sqlite3
import sys
import XMLgetClass as XML

#Where is the DB located?
str=''
dbPath = []
#dbPath.append('/home/bhaines/Documents/HackerSchool/Python/XMLparse/') # This can be left out
dbPath.append('curveDB') #without the path, this db is created in the current directory
dbLoc = str.join(dbPath)

#These are the fields for the curves
listofKeys = ['id', 'NEW_DATE','BC_1MONTH','BC_3MONTH','BC_6MONTH','BC_1YEAR','BC_2YEAR','BC_3YEAR','BC_5YEAR','BC_7YEAR'
	,'BC_10YEAR','BC_20YEAR','BC_30YEAR']

#Retrieve the curves by calling the curveGet class:
try:
	x = XML.curveGet() #This goes out onto the net to get yield curves
except Exception as e:
	print("Error with getting the curves: ", e[0])
	sys.exit

def updateCurveDB(oneDay):

	y=[]
	for s in listofKeys:
		y.append(oneDay[s]) #s is each key, so calling oneDay[s] get the value associated with the key
	#Assign values to the variables
	cid = y[0]
	cDate = y[1][:10] # Shows the first 10 positions of the date string
	month1 = y[2]
	month3 = y[3]
	month6 = y[4]
	year1 = y[5]
	year2 = y[6]
	year3 = y[7]
	year5 = y[8]
	year7 = y[9]
	year10 = y[10]
	year20 = y[11]
	year30 = y[12]
	print(cid, cDate,month1,month3,month6,year1,year2,year3,year5,year7,year10,year20,year30)

	#Instert all of this to the database IF the cid is not already present.
	db = None
	try:
		#create or open existing db
		db = sqlite3.connect(dbLoc)
		# Get a cursor object
		cursor = db.cursor()
		#This is an SQL string to create a table in the database.
		cursor.execute('''CREATE TABLE IF NOT EXISTS curves(id INTEGER unique PRIMARY KEY, curveDate TEXT unique, 
			month1 REAL,month3 REAL,month6 REAL,year1 REAL,year2 REAL,year3 REAL,year5 REAL,year7 REAL,year10 REAL,year20 REAL
			,year30 REAL)''')
		db.commit()

		#I need to make changes to this so that only new id's are added to the table
		cursor.execute('''INSERT INTO curves(id, curveDate, month1, month3, month6, year1, year2, year3, year5, year7, year10
			, year20, year30) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (cid, cDate, month1, month3, month6, year1, year2, 
			year3, year5, year7, year10, year20, year30))
		db.commit()

	except Exception as e2:
		print("Error: ", e2[0])
		sys.exit
	finally:
		db.close

def getCurve():

	#To Do, be able to specify which column you want and/or return only
	#that column
	db = None
	try:
		#Open existing db
		db = sqlite3.connect(dbLoc)
		# Get a cursor object
		cursor = db.cursor()

		#Call the db
		cursor.execute('''SELECT * FROM curves ORDER BY id''')

		for row in cursor:
			print(row)

	except Exception as e:
		print("Error: ", e)
		sys.exit
	finally:
		db.close


def main():
	#Take curveList and turn it into something useful, one day's curve at a time.
	for i in x.curveList: #i is a dict
		updateCurveDB(i)

	# getCurve()

if __name__ == '__main__': main()