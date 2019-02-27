import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

sql = "select m.name,m.position,t.city,t.name from nfl_database_teams t, nfl_database_players p, player_model m where m.name=p.name and m.position=p.position and p.team_id=t.id"
mycursor = mydb.cursor()
mycursor.execute(sql)
results = mycursor.fetchall()

for result in results:
	name = result[0]
	position = result[1]
	fullteam = result[2]+" "+result[3]
	sql = "update player_model m set m.team = %s where m.name = %s and m.position = %s"
	val = (fullteam,name,position)
	mycursor.execute(sql,val)

mydb.commit()
