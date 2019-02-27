import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

f = open("lineups.txt","r")
with open('dklinesup.csv', 'w',encoding="utf-8", newline='') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
	contents = f.readlines()
	counter = 0
	lineups = []
	lineup = []
	for line in contents:
		if line=="\n":
			lineups.append(lineup)
			lineup = []
		else:
			line = line.strip()
			lineup.append(line)

	def write_lineup(lineup):
		if len(lineup) != 11:
			print("error with lineup")
			# print(lineup)
		else:
			row = []
			index = 0
			for player in lineup:
				player = player.split(',')[0]
				if index > 8:
					break
				if index < 8:
					sql = "select dk_id from player_model where name like %s"
					val = ('%'+player+'%',)
				if index==8:
					sql = "select dk_id from player_model where team=%s"
					val = (player,)
				mycursor = mydb.cursor()
				mycursor.execute(sql,val)
				result = mycursor.fetchone()
				if result:
					dk_id = result[0]
				else:
					dk_id = player
				row.append(str(dk_id))
				index += 1
			lineup = []
			lineup.append(row[0])
			lineup.append(row[1])
			lineup.append(row[2])
			lineup.append(row[4])
			lineup.append(row[5])
			lineup.append(row[6])
			lineup.append(row[7])
			lineup.append(row[3])
			lineup.append(row[8])
			row = ','.join(lineup)
			print(row)
			row = row.strip()
			csvwriter.writerow(row)

	for lineup in lineups:
		write_lineup(lineup)
