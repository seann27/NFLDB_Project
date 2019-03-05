import mysql.connector
import logging
import sys
import datetime

# initialize logger
timeid = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
logfile = ('logs/run_SQL_DRIVER_'+timeid+'.log')
logging.basicConfig(level=logging.DEBUG,filename=logfile,filemode='w',format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')

# initialize db connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
mycursor = mydb.cursor()

def get_file_contents(file):
	# Open and read the file as a single buffer
	fd = open(file, 'r')
	sqlFile = fd.read().strip()
	fd.close()
	logging.debug(file)
	return sqlFile

# makes changes within the database
def executeScript(file):
	sqlCommand = get_file_contents(file)

	# executes sql command
	try:
		mycursor.execute(sqlCommand)
	except mysql.connector.Error as msg:
		print("Command skipped: ",sqlCommand, msg)
		logging.error(msg)

	mydb.commit()

# needs testing
def executeSelect(file,params=None):

	# executes a specific command in the file
	sqlCommand = get_file_contents(file)
	try:
		mycursor.execute(sqlCommand,params=params,multi=True)
		results = mycursor.fetchall()
	except mysql.connector.Error as msg:
		print("Command skipped: ",command, msg)
		logging.error(msg)
	return results

# needs testing
def executeUpdate(file,params=None):
    	# executes a specific command in the file
    	sqlCommand = get_file_contents(file)
    	try:
    		mycursor.execute(sqlCommand,params=params,multi=True)
    		results = mycursor.fetchall()
    	except mysql.connector.Error as msg:
    		print("Command skipped: ",command, msg)
    		logging.error(msg)

        mydb.commit()
