"""
This will create a DB if one does not already exist, then populate it with all of the
yield curve data from XMLgetClass variable .curveList[]
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
print(dbLoc) #Here it is...

listofKeys = ['id', 'NEW_DATE','BC_1MONTH','BC_3MONTH','BC_6MONTH','BC_1YEAR','BC_2YEAR','BC_3YEAR','BC_5YEAR','BC_7YEAR'
	,'BC_10YEAR','BC_20YEAR','BC_30YEAR']


#Call the curveGet class:
try:
	x = XML.curveGet() #this goes out onto the net to get yield curves
except Exception as e:
	print("Error with getting the curves: ", e[0])
	sys.exit


#Take curveList and turn it into something useful, one day's curve at a time.
for i in x.curveList:
	x=[]
	for s in listofKeys:
		x.append(i[s])
	#Assign values to the variables
	cid = x[0]
	cDate = x[1][:10] # Shows the first 10 positions of the date string
	month1 = x[2]
	month3 = x[3]
	month6 = x[4]
	year1 = x[5]
	year2 = x[6]
	year3 = x[7]
	year5 = x[8]
	year7 = x[9]
	year10 = x[10]
	year20 = x[11]
	year30 = x[12]
	print(cid, cDate,month1,month3,month6,year1,year2,year3,year5,year7,year10,year20,year30)

	#Instert all of this to the database IF the cid is not already present.
	db = None
	try:
		#create or open existing db
		db = sqlite3.connect(dbLoc)
		# Get a cursor object
		cursor = db.cursor()
		#This is an SQL string to create a table in the database
		cursor.execute('''CREATE TABLE IF NOT EXISTS curves(id INTEGER unique PRIMARY KEY, curveDate TEXT unique, 
			month1 REAL,month3 REAL,month6 REAL,year1 REAL,year2 REAL,year3 REAL,year5 REAL,year7 REAL,year10 REAL,year20 REAL
			,year30 REAL)''')
		db.commit()

		cursor.execute('''INSERT INTO curves(id, curveDate, month1, month3, month6, year1, year2, year3, year5, year7, year10
			, year20, year30) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (cid, cDate, month1, month3, month6, year1, year2, 
			year3, year5, year7, year10, year20, year30))
		db.commit()

	except Exception as e2:
		print("Error: ", e2[0])
		sys.exit
	finally:
		db.close





