import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

mycursor = mydb.cursor()

def get_file_contents(file):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
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
        except OperationalError, msg:
            print "Command skipped: ", msg
    mydb.commit()

def executeSelect(file,command,args):
    # all SQL commands (split on ';')
    # executes a specific command in the file
    sqlCommands = get_file_contents(file).split(';')[command]
    params=None
    if args:
        params=args
    iterator = mycursor.execute(command,params=params,multi=True)
    return iterator
