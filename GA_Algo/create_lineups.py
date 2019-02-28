import mysql.connector
import random
from pyeasyga import pyeasyga

class Player:
	def __init__(self,name,rank,salary):
		self.name = name
		self.rank = rank
		self.salary = salary
		self.qb = 0
		self.rb = 0
		self.wr = 0
		self.te = 0
		self.k = 0
		self.dst = 0

player_stats_list = []
player_names_list = []
def get_players(pos):
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="nfl_db"
	)
	sql = "select * from player_model where position = %s and fp_rank is not null order by fp_rank asc"
	mycursor = mydb.cursor()
	val = (pos,)
	mycursor.execute(sql,val)
	results = mycursor.fetchall()
	for item in results:
		name = item[2]
		rank = item[5]
		rank = 500-rank
		salary = item[6]
		obj = Player(name,rank,salary)
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
		player_stats_list.append((rank,salary,obj.qb,obj.rb,obj.wr,obj.te,obj.k,obj.dst))
		player_names_list.append(name)

# get_players('QB')
get_players('RB')
get_players('WR')
get_players('TE')
# get_players('K')
# get_players('D')

# print(len(player_list))
# print(player_names_list)
#
ga = pyeasyga.GeneticAlgorithm(player_stats_list)        # initialise the GA with data

def create_individual(data):
	list = []
	one = 0
	for x in range(len(data)):
		val = random.randint(0, 1)
		if val == 1:
			one += 1
		if one > 6:
			val = 0
		list.append(val)
	return list

ga.create_individual = create_individual
ga.population_size = 100000                  # increase population size to 200 (default value is 50)

# print(player_names_list)
# # define a fitness function
def fitness(individual, data):
	rank,salary,qb,rb,wr,te,k,dst = 0,0,0,0,0,0,0,0
	for (selected, item) in zip(individual, data):
		if selected:
			rank += item[0]
			salary += item[1]
			qb += item[2]
			rb += item[3]
			wr += item[4]
			te += item[5]
			k += item[6]
			dst += item[7]
	if salary > 50000 or qb > 1 or rb > 3 or wr > 3 or te > 2 or k > 1 or dst > 1:
		rank = 0
	return rank
#
ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
# print(ga.best_individual() )                 # print the GA's best solution

results = ga.best_individual()
players = results[1]
#
total_sal = 0
total_rank = 0
for i in range(1, len(players)):
	if players[i] > 0:
		print(player_names_list[i]+"\t"+str(player_stats_list[i][0])+"\t"+str(player_stats_list[i][1]))
		total_sal += player_stats_list[i][1]
		total_rank += player_stats_list[i][0]
print()
print(total_sal)
print(total_rank)



# # setup data
# data = [(821, 0.8, 118), (1144, 1, 322), (634, 0.7, 166), (701, 0.9, 195),
#         (291, 0.9, 100), (1702, 0.8, 142), (1633, 0.7, 100), (1086, 0.6, 145),
#         (124, 0.6, 100), (718, 0.9, 208), (976, 0.6, 100), (1438, 0.7, 312),
#         (910, 1, 198), (148, 0.7, 171), (1636, 0.9, 117), (237, 0.6, 100),
#         (771, 0.9, 329), (604, 0.6, 391), (1078, 0.6, 100), (640, 0.8, 120),
#         (1510, 1, 188), (741, 0.6, 271), (1358, 0.9, 334), (1682, 0.7, 153),
#         (993, 0.7, 130), (99, 0.7, 100), (1068, 0.8, 154), (1669, 1, 289)]
#
# ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data
# ga.population_size = 200                    # increase population size to 200 (default value is 50)
#
# # define a fitness function
# def fitness(individual, data):
# 	# print(individual)
# 	weight, volume, price = 0, 0, 0
# 	for (selected, item) in zip(individual, data):
# 		if selected:
# 			weight += item[0]
# 			volume += item[1]
# 			price += item[2]
# 	if weight > 12210 or volume > 12:
# 		price = 0
# 	return price
#
# ga.fitness_function = fitness               # set the GA's fitness function
# ga.run()                                    # run the GA
# print(ga.best_individual() )                 # print the GA's best solution
