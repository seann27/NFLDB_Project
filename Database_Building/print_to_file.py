import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)
mycursor = mydb.cursor()

def download(output_file,position):
	sql = "select p.name,p.position,p.team,p.opp,p.fp_rank,e.proj_points,p.dk_salary from player_model p, espn_player_projections e where p.id=e.id and p.week=14 and p.played='n' and p.position=%s and p.fp_rank is not null order by p.dk_salary desc;"
	val = (position,)
	mycursor.execute(sql,val)
	results = mycursor.fetchall()
	f = open(output_file,'w')
	f.write("--------------------------------------------------------------------------------\n")
	f.write("FORMAT:\n")
	f.write("NAME,POSITION,TEAM,OPP,FANTASY PROS RANK,ESPN PROJ POINTS, DRAFT KINGS SALARY\n")
	f.write("--------------------------------------------------------------------------------\n")
	for result in results:
		f.write(result[0]+","+result[1]+","+result[2]+","+result[3]+","+str(result[4])+","+str(result[5])+","+str(result[6])+"\n")
	f.close()

def download_d(output_file):
	position = 'D'
	sql = "select p.name,p.position,p.team,p.opp,p.fp_rank,e.proj_points,p.dk_salary from player_model p, espn_defense_projections e where p.id=e.id and p.week=14 and p.played='n' and p.position=%s and p.fp_rank is not null order by p.dk_salary desc;"
	val = (position,)
	mycursor.execute(sql,val)
	results = mycursor.fetchall()
	f = open(output_file,'w')
	f.write("--------------------------------------------------------------------------------\n")
	f.write("FORMAT:\n")
	f.write("NAME,POSITION,TEAM,OPP,FANTASY PROS RANK,ESPN PROJ POINTS, DRAFT KINGS SALARY\n")
	f.write("--------------------------------------------------------------------------------\n")
	for result in results:
		f.write(result[0]+","+result[1]+","+result[2]+","+result[3]+","+str(result[4])+","+str(result[5])+","+str(result[6])+"\n")
	f.close()
	
download('week14_QBs.txt','QB')
download('week14_RBs.txt','RB')
download('week14_WRs.txt','WR')
download('week14_TEs.txt','TE')
download_d('week14_DSTs.txt')

def download_lineups(output_file):
	f = open(output_file,'w')
	sql = "select QB,RB1,RB2,WR1,WR2,WR3,TE,FLEX,DST,fp_rank,proj_points,dk_salary from optimal_lineups order by proj_points desc"
	mycursor.execute(sql)
	results = mycursor.fetchall()
	f.write("----------------------------------------------\n")
	f.write("ORDERED BY PROJECTED POINTS\n")
	f.write("----------------------------------------------\n")
	f.write("FORMAT:\n")
	f.write("QB\nRB1\nRB2\nWR1\nWR2\nWR3\nTE\nFLEX\nDST\nCOMBINED FANTASY PROS RANK\nCOMBINED ESPN PROJ POINTS\nCOMBINED SALARY\n")
	f.write("----------------------------------------------\n")
	for result in results:
		f.write(result[0]+"\n"+result[1]+"\n"+result[2]+"\n"+result[3]+"\n"+result[4]+"\n"+result[5]+"\n"+result[6]+"\n"+result[7]+"\n"+result[8]+"\n\nRANK: "+str(result[9])+"\nPROJ POINTS: "+str(result[10])+"\n"+str(result[11])+"\n\n")
	f.close()

download_lineups('week14_lineups.txt')
