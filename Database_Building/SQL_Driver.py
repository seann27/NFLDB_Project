import mysql.connector
import sys

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
    return sqlFile

# makes changes within the database
def executeScript(file):
    # all SQL commands (split on ';')
    sqlCommands = get_file_contents(file).split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            mycursor.execute(command)
        except mysql.connector.Error as msg:
            print("Command skipped: ",command, msg)
    mydb.commit()

def executeSelect(file,params=None,command=0):
    # all SQL commands (split on ';')
    # executes a specific command in the file
    sqlCommands = get_file_contents(file).split(';')[command]
    try:
        mycursor.execute(command,params=params,multi=True)
        results = mycursor.fetchall()
    except mysql.connector.Error as msg:
        print("Command skipped: ",command, msg)
        results = (msg,)
    return results

if __name__ == "__main__":
	command = sys.argv[1]
	if command == 'create':
		executeScript('SQL_Scripts/create_base_tables.sql')
	elif command == 'drop':
		executeScript('SQL_Scripts/drop_base_tables.sql')
	else:
		print("no command of that type found.")
