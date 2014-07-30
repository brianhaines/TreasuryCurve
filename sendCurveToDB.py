"""
This will create a DB if one does not already exist, then populate it with all of the
yield curve data from XMLgetClass variable .curveList[]
"""

import sqlite3

#Where is the DB located?
str=''
dbPath = []
#dbPath.append('/home/bhaines/Documents/HackerSchool/Python/XMLparse/') # This can be left out
dbPath.append('curveDB') #without the path, this db is created in the current directory
dbLoc = str.join(dbPath)
print(dbLoc) #Here it is...

#Create new or open existing database
try:
	db = sqlite3.connect(dbLoc)
except Exception as e:
	db.rollback()
	raise e
finally:
	db.close

