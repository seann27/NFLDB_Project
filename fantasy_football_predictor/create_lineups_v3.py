import mysql.connector
import random
from pyeasyga import pyeasyga
from random import shuffle
import time

start = time.time()

season = 2018
week = 14

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="nfl_db"
)

player_stats_list = []
player_names_list = []

# this class isn't used
class Player:
	def __init__(self,name,pos,fp_rank,proj_points,salary):
		self.name = name
		self.pos = pos
		self.fp_rank = fp_rank
		self.proj_points = proj_points
		self.salary = salary
		self.qb = 0
		self.rb = 0
		self.wr = 0
		self.te = 0
		self.dst = 0

def get_players(pos):
	total = 0
	if pos == 'D':
		sql = "select e.name, p.fp_rank, e.proj_points, p.dk_salary from espn_defense_projections e, player_model p where p.id=e.id and p.fp_rank is not null and p.week = %s and p.played='n' order by proj_points desc"
		mycursor = mydb.cursor()
		val = (week,)
		mycursor.execute(sql,val)
		results = mycursor.fetchall()
	else:
		sql = "select e.name, p.fp_rank, e.proj_points, p.dk_salary from espn_player_projections e, player_model p where p.id=e.id and p.fp_rank is not null and p.position=%s and p.week = %s and p.played='n' order by proj_points desc"
		mycursor = mydb.cursor()
		val = (pos,week,)
		mycursor.execute(sql,val)
		results = mycursor.fetchall()
	for item in results:
		name = item[0]
		fp_rank = item[1]
		proj_points = item[2]
		salary = item[3]
		obj = Player(name,pos,fp_rank,proj_points,salary)
		if pos == 'QB':
			obj.qb = 1
		if pos == 'RB':
			obj.rb = 1
		if pos == 'WR':
			obj.wr = 1
		if pos == 'TE':
			obj.te = 1
		if pos == 'K':
			obj.k = 1
		if pos == 'D':
			obj.dst = 1
		player_stats_list.append((name,pos,fp_rank,proj_points,salary,obj.qb,obj.rb,obj.wr,obj.te,obj.dst))
		total+=1
	return total

qbs = get_players('QB')
rbs = get_players('RB')
wrs = get_players('WR')
te = get_players('TE')
dst = get_players('D')

ga = pyeasyga.GeneticAlgorithm(player_stats_list,population_size=1000,generations=200)        # initialize the GA with data

def create_individual(data):
	list = []
	map = []
	num_qbs = qbs
	num_rbs = rbs
	num_wrs = wrs
	num_te = te
	num_dst = dst
	num_rbs += num_qbs
	num_wrs += num_rbs
	num_te += num_wrs
	num_dst += num_te
	#qb
	map.append(random.randint(0,num_qbs))
	# 2 rbs
	map.append(random.randint(num_qbs,num_rbs))
	map.append(random.randint(num_qbs,num_rbs))
	# 3 wrs
	map.append(random.randint(num_rbs,num_wrs))
	map.append(random.randint(num_rbs,num_wrs))
	map.append(random.randint(num_rbs,num_wrs))
	# 1 te
	map.append(random.randint(num_wrs,num_te))
	# 1 flex
	map.append(random.randint(num_qbs,num_te))
	# 1 dst
	map.append(random.randint(num_te,num_dst))
	for x in range(len(data)):
		val=0
		if x in map:
			val=1
		list.append(val)
	return list

ga.create_individual = create_individual

# # define a fitness function
def fitness(individual, data):
	name,pos,fp_rank,proj_points,salary,qb,rb,wr,te,dst = '','',0,0,0,0,0,0,0,0
	for (selected, item) in zip(individual, data):
		total = 0
		if selected:
			fp_rank += item[2]
			proj_points += item[3]
			salary += item[4]
			qb += item[5]
			rb += item[6]
			wr += item[7]
			te += item[8]
			dst += item[9]
			total += 1
	if salary > 50000 or qb > 1 or rb > 3 or wr > 3 or te > 1 or dst > 1:
		proj_points = 0
	return proj_points

ga.fitness_function = fitness

def process_lineup(list):
	qb = ''
	rb1 = ''
	rb2 = ''
	wr1 = ''
	wr2 = ''
	wr3 = ''
	te = ''
	flex = ''
	dst = ''
	num_rbs = 0
	num_wrs = 0
	num_te = 0
	for i in range(9):
		item = list[i].split(',')
		position = item[1]
		player = item[0]
		if position == 'QB':
			qb = player
		if position == 'RB':
			if num_rbs == 0:
				rb1 = player
			elif num_rbs ==  1:
				rb2 = player
			elif num_rbs == 2:
				flex = player
			num_rbs += 1
		if position == 'WR':
			if num_wrs == 0:
				wr1 = player
			elif num_wrs == 1:
				wr2 = player
			elif num_wrs == 2:
				wr3 = player
			elif num_wrs == 3:
				flex = player
			num_wrs += 1
		if position == 'TE':
			if num_te == 0:
				te = player
			elif num_te == 1:
				flex = player
			num_te += 1
		if position == 'D':
			dst = player
	total_rank = list[9].split(': ')[1]
	total_proj_points = list[10].split(': ')[1]
	total_salary = list[11].split(': ')[1]
	sql = "INSERT INTO optimal_lineups (season,week,QB,RB1,RB2,WR1,WR2,WR3,TE,FLEX,DST,fp_rank,proj_points,dk_salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (season,week,qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst,total_rank,total_proj_points,total_salary)
	mycursor = mydb.cursor()
	mycursor.execute(sql,val)
	mydb.commit()

for x in range(30):
	ga.run()
	results = ga.best_individual()
	players = results[1]
	total_sal = 0
	total_points = 0
	total_rank = 0
	strings = []
	for i in range(0, len(players)):
		if players[i] > 0:
			strings.append(player_stats_list[i][0]+","+player_stats_list[i][1]+", rank: "+str(player_stats_list[i][2])+", proj. points: "+str(player_stats_list[i][3])+", draft kings salary: $"+str(player_stats_list[i][4]))
			total_rank += player_stats_list[i][2]
			total_points += player_stats_list[i][3]
			total_sal += player_stats_list[i][4]
	if len(strings) == 9:
		strings.append("Total Rank: "+str(total_rank))
		strings.append("Total Projected Points: "+str(total_points))
		strings.append("Total Cost: $"+str(total_sal))
		process_lineup(strings)

end = time.time()
print("Time elapsed: "+str((end-start)/60)+" minutes")
