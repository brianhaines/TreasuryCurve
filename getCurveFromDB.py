"""
This will retrieve specified curves from the database.
"""
import sqlite3
import sys


#Where is the DB located?
str=''
dbPath = []
#dbPath.append('/home/bhaines/Documents/HackerSchool/Python/XMLparse/') # This can be left out
dbPath.append('curveDB') #without the path, this db is created in the current directory
dbLoc = str.join(dbPath)
#print(dbLoc) #Here it is...



db = None
try:
	#create or open existing db
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

