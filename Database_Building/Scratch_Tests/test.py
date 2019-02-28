import random

list = []
map = []
one = 0
for x in range(9):
	val = random.randint(0,99)
	while val in map:
		val = random.randint(0,99)
	print(val)
	map.append(val)
print("&&&&&&&&&&&&&&&*^*&^*")
for x in range(100):
	if x in map:
		print(str(x)+" - match")
	else:
		print(x)
print()
print(len(map))
print()
for x in range(len(map)):
	print(x)
