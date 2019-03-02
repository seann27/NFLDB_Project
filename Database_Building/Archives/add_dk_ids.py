import csv
import mysql.connector
player_names = []
dk_ids = []
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
with open('dk_ids.csv', 'rt') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in csvreader:
		row = ' '.join(row)
		values = row.split(',')
		fullname = values[0].strip().split()
		id = values[1].strip()
		if len(fullname) > 1:
			name = fullname[0]+" "+fullname[1]
		else:
			''.join(fullname)
			name = ''.join(fullname)
		print(name+" - "+str(id))
		mycursor = mydb.cursor()
		sql = "update player_model set dk_id=%s where name like %s"
		val = (id,'%'+name+'%',)
		mycursor.execute(sql,val)
		sql = "update player_model set dk_id=%s where team = %s"
		val = (id,name,)
		mycursor.execute(sql,val)
mydb.commit()
