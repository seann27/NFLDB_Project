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
	# all SQL commands (split on ';')
	sqlCommands = get_file_contents(file).split(';')

	# Execute every command from the input file
	for command in sqlCommands:
		command = command.strip()
		logging.debug(command)
		# This will skip and report errors
		# For example, if the tables do not yet exist, this will skip over
		# the DROP TABLE commands
		try:
			mycursor.execute(command)
			logging.debug("Executed successfully.")
		except mysql.connector.Error as msg:
			print("Command skipped: ",command, msg)
			logging.error(msg)
	mydb.commit()

def executeSelect(file,params=None,command=0):
	# all SQL commands (split on ';')
	# executes a specific command in the file
	sqlCommands = get_file_contents(file)
	logging.debug(sqlCommands)
	try:
		mycursor.execute(command,params=params,multi=True)
		results = mycursor.fetchall()
		logging.debug("Executed Successfully")
	except mysql.connector.Error as msg:
		print("Command skipped: ",command, msg)
		logging.error(msg)
	return results

if __name__ == "__main__":
	command = sys.argv[1]
	if command == 'create':
		executeScript('SQL_Scripts/create_base_tables.sql')
	elif command == 'drop':
		executeScript('SQL_Scripts/drop_base_tables.sql')
	else:
		print("no command of that type found.")
