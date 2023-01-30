import sys
sys.setrecursionlimit(100)
class Node:
	children = []
	x_cord = None
	y_cord = None
	elevation = None

	def __init__(self, x, y, parent=None):
		self.x_cord = x
		self.y_cord = y
		self.parent = parent

	def __eq__(self, other):
		return self.x_cord == other.x_cord and self.y_cord == other.y_cord

	def __str__(self):
		return "(" + str(self.x_cord) + "," + str(self.y_cord) + ")" 

def get_surrounding_locations(x_cord, y_cord):
	north = south = east = west = north_east = north_west = south_west = south_east = None
	surr = {}

	surr["north"] =  (x_cord, y_cord - 1)
	surr["south"] = (x_cord, y_cord   + 1)
	surr["east"] = (x_cord + 1, y_cord)
	surr["west"] = (x_cord - 1, y_cord)
	surr["north_east"] = (x_cord + 1, y_cord - 1)
	surr["north_west"] = (x_cord - 1, y_cord - 1)
	surr["south_west"] = (x_cord - 1, y_cord + 1)
	surr["south_east"] = (x_cord + 1, y_cord + 1)

	# Eliminate out of bounds cells
	for direction in surr:
	
		if -1 in surr[direction] or surr[direction][0] == width  or surr[direction][1] == height:
			surr[direction] = None

	return surr

def is_move_allowed(start_position, end_position):
	# Stamina check
	#print("Move allowed from " + str(start_position) + "to " + str(end_position) + "??")
	is_allowed = False
	if end_position is None:
		#print(is_allowed)
		return False
	start_x, start_y = start_position
	dest_x, dest_y = end_position

	is_dest_tree = True if ski_map[dest_y][dest_x] < 0 else False


	if ski_map[start_y][start_x] >= abs(ski_map[dest_y][dest_x]) and is_dest_tree:
		# Tree height check
		is_allowed = True
	elif ski_map[start_y][start_x] <= ski_map[dest_y][dest_x] and not is_dest_tree:
		# Stamina check
		if stamina >= ski_map[dest_y][dest_x] - ski_map[start_y][start_x]:
			is_allowed = True
	elif ski_map[start_y][start_x] >= ski_map[dest_y][dest_x] and not is_dest_tree:
		is_allowed = True

	#print(is_allowed)
	return is_allowed


def get_movable_locations(position):
	
	x_cord, y_cord = position

	surrounding_locations = get_surrounding_locations(x_cord, y_cord)
	#print("surrounding_locations: ", str(surrounding_locations))
	movable_locations = []

	for surrounding_location in surrounding_locations:
		is_movable = is_move_allowed(position, surrounding_locations[surrounding_location])

		if is_movable:
			movable_locations.append(surrounding_locations[surrounding_location])

	return movable_locations

def convert_locations_to_nodes(locations, parent):
	nodes = []
	for location in locations:
		node = Node(x=location[0], y=location[1], parent=parent)
		nodes.append(node)

	return nodes
	


def bfs(end, parent=None, visited=[], cost=0, enqueued=[]):	
	node = enqueued.pop(0)
	cost = cost+1
	
	if parent is not None:	
		node.parent = parent

	visited.append((node.x_cord, node.y_cord))
	print("Visited: " + str(visited))

	print(f"Visiting Node({node.x_cord},{node.y_cord}) with elevation")
	print(ski_map[node.y_cord][node.x_cord])

	movable_locations = get_movable_locations((node.x_cord, node.y_cord))
	movable_nodes = convert_locations_to_nodes(movable_locations, parent)
	print("Movable nodes: ")
	print_node_list(movable_nodes)
	
	for movable_node in movable_nodes:
		if movable_node not in enqueued:
			enqueued.append(movable_node)
	

	print("enqueued: ")
	print_node_list(enqueued)
	print("****")
	if (node.x_cord, node.y_cord) == end:
	 	print("Arrived at destination")
	 	return cost
	else:
		return bfs(end, parent=node, cost=cost, visited=visited, enqueued=enqueued)

	#print("ENd: " + str(end))

	# for movable_location in  movable_locations:
	# 	#print("Movable: " + str(movable_location))
	# 	if movable_location is end:
	# 		print("Arrived at destination")
	# 	if movable_location is not end and movable_location not in visited:
	# 		next_node = Node(x=movable_location[1], y=movable_location[0], parent=node)

	# 		if next_node not in visited:
	# 			cost = cost + 1
	# 			enqueued.append(next_node)
	# 			cost = bfs(end, parent=node, cost=cost, visited=visited, enqueued=enqueued)
	# 	else:
	# 		return 1

	return cost

def print_map(ski_map):
	for row in ski_map:
		print(row)

def print_node_list(nodes):
	for node in nodes:
		print(str(node))

file = open('input.txt','r')
file_lines = file.readlines()


# Convert read bytes into ints wherever applicable
algorithm = file_lines[0]
width, height = file_lines[1].strip().split(" ")
width = int(width)
height = int(height)

start_x, start_y = file_lines[2].strip().split(" ")
start_x = int(start_x)
start_y = int(start_y)

stamina = int(file_lines[3])
stamina = int(stamina)

num_lodges = int(file_lines[4])

lodge_locs = []
counter = 5
for i in range(5, 5 + num_lodges):
	counter = counter + 1
	loc_x, loc_y = file_lines[i].strip().split(" ")
	loc_x = int(loc_x)
	loc_y = int(loc_y)
	lodge_locs.append((loc_x, loc_y))


ski_map = [] # Supposed to be an array of arrays

for i in range(0, height):
	ski_map_row = file_lines[counter].strip().split(" ")
	ski_map_row = [int(e) for e in ski_map_row]
	ski_map.append(ski_map_row)
	counter += 1



for lodge in lodge_locs:
	if algorithm == "BFS":
		optimal_cost = find_bfs_cost(start_loc, lodge_loc)


print(print_map(ski_map))
print("Stamina: "+ str(stamina))

#print("Movable locations for 4, 4")

#print(get_movable_locations((4,4)))
start_node = Node(x=4, y=4)
print("Cystom: " + str(start_node))
print("****")
print(bfs((2,1), enqueued=[start_node]))
