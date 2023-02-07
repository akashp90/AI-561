import sys
import random
import math
import bisect
#sys.setrecursionlimit(10000)
class Node:
    children = []
    x_cord = None
    y_cord = None
    elevation = None
    cost = 0
    momentum = 0

    def __init__(self, x, y, parent=None, cost=0, momentum=0):
        self.x_cord = x
        self.y_cord = y
        self.parent = parent
        self.cost = cost
        self.momentum = momentum
        self.elevation = ski_map[y][x]

    def __eq__(self, other):
        return self.x_cord == other.x_cord and self.y_cord == other.y_cord and self.momentum == other.momentum

    def __str__(self):
        return "(" + str(self.x_cord) + "," + str(self.y_cord) + ")" 

def get_surrounding_locations(x_cord, y_cord):
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

def is_move_allowed(start_position, end_position, momentum=None):
    # Stamina check
    #print("Move allowed from " + str(start_position) + "to " + str(end_position) + "??")
    is_allowed = False
    if end_position is None:
        return False

    start_x, start_y = start_position
    dest_x, dest_y = end_position

    is_dest_tree = True if ski_map[dest_y][dest_x] < 0 else False
    #print("Values")
    #print("abs(ski_map[start_y][start_x])" + str(abs(ski_map[start_y][start_x])))


    if abs(ski_map[start_y][start_x]) >= abs(ski_map[dest_y][dest_x]) and is_dest_tree:
        # Tree height check
        is_allowed = True
    elif abs(ski_map[start_y][start_x]) <= ski_map[dest_y][dest_x] and not is_dest_tree and momentum is None:
        # Stamina check
        if stamina >= ski_map[dest_y][dest_x] - abs(ski_map[start_y][start_x]):
            is_allowed = True
    elif abs(ski_map[start_y][start_x]) >= ski_map[dest_y][dest_x] and not is_dest_tree:
        is_allowed = True

    if momentum is not None:
        elevation_change = ski_map[dest_y][dest_x] - ski_map[start_y][start_x]
        if elevation_change <= stamina + momentum:
            is_allowed = True

    #print("Move allowed" + str(is_allowed))
    return is_allowed


def get_movable_locations(position, random_order=False, momentum=None):
    x_cord, y_cord = position

    surrounding_locations = get_surrounding_locations(x_cord, y_cord)

    if random_order:
        location_keys = list(surrounding_locations.keys())
        shuffled_locations = {}
        random.shuffle(location_keys)

        for k in location_keys:
          shuffled_locations[k] = surrounding_locations[k]
        
        surrounding_locations = shuffled_locations
    movable_locations = []

    for surrounding_location in surrounding_locations:
        is_movable = is_move_allowed(position, surrounding_locations[surrounding_location], momentum)

        if is_movable:
            movable_locations.append(surrounding_locations[surrounding_location])

    return movable_locations

def calculate_momentum(elevation_change):
    if elevation_change <= 0:
        return 0
    elif elevation_change > 0:
        return max(0, elevation_change)
    else:
        raise Exception("Whoops! This wasn't supposed to happen")

def elevation_change_cost(start, end):
    elevation_change = ski_map[end[1]][end[0]] - ski_map[start[1]][start[0]]
    momentum = calculate_momentum(elevation_change)

    if elevation_change <= momentum:
        return 0
    elif elevation_change > momentum:
        return max(0, elevation_change - momentum)
    else:
        raise Exception("Whoops! This wasn't supposed to happen")


def euc_distance(point_1, point_2):
    distance = (point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2
    return math.sqrt(distance)

def get_cost_to_node(start, end, destination):
    move_cost = 0
    if abs(start[0] - end[0]) + abs(start[1] - end[1]) == 1:
        move_cost = 10
    elif abs(start[0] - end[0]) + abs(start[1] - end[1]) >= 1:
        move_cost = 14

    move_cost += elevation_change_cost(start, end)

    # Heuristic
    move_cost += euc_distance(end, destination)
    
    return move_cost


def convert_locations_to_nodes(locations, parent, cost=0, destination=None, momentum=0):
    nodes = []
    for location in locations:
        cost_to_node = None
        if parent is not None and destination is not None:
            cost_to_node = parent.cost + get_cost_to_node((parent.x_cord, parent.y_cord), location, destination)
        node = Node(x=location[0], y=location[1], parent=parent, cost=cost_to_node)
        nodes.append(node)

    return nodes
    

def trace_to_root(node_list):
    if len(node_list) == 0:
        return []

    leaf = node_list[-1]
    node = leaf
    path = []

    while(1):
        if node.parent is None:
            path.append(node)
            path.reverse()
            return path

        
        path.append(node)
        node = node.parent

def bfs(end, visited=[], cost=0, enqueued=[]):
    while 1:
        if len(enqueued) <= 0:
            return "FAIL", []

        node = enqueued.pop(0)
        
        cost = cost+1

        visited.append(node)
        movable_locations = get_movable_locations((node.x_cord, node.y_cord), random_order=True)
        movable_nodes = convert_locations_to_nodes(movable_locations, node)
        

        for movable_node in movable_nodes:
            if (movable_node.x_cord, movable_node.y_cord) == end:
                
                visited.append(movable_node)
                return (cost + 1, visited)
            elif movable_node not in visited:
                enqueued.append(movable_node)


def ucs(end, visited=[], cost=0, enqueued=[]):  
    while 1:
        if len(enqueued) <= 0:
            return "FAIL", []

        node = enqueued.pop(0)
        
        cost = cost+1

        visited.append(node)
        movable_locations = get_movable_locations((node.x_cord, node.y_cord), random_order=False)
        movable_nodes = convert_locations_to_nodes(movable_locations, node)
        

        for movable_node in movable_nodes:
            if (movable_node.x_cord, movable_node.y_cord) == end:
                
                visited.append(movable_node)
                return (cost + 1, visited)
            elif movable_node not in visited:
                enqueued.append(movable_node)


def a_star(end, enqueued=[]):
    visited = []
    momentum = 0
    
    while 1:
        print("Enq")
        print_node_list(enqueued)
        if len(enqueued) <= 0:
            return "FAIL", []

        node = enqueued.pop(0)
        cost = node.cost
        previous_node = node.parent

        if previous_node is not None:
            elevation_change = previous_node.elevation - node.elevation
            print("Elevation change:" + str(elevation_change))
            momentum = calculate_momentum(elevation_change)

        print("********")
        print("Node: " + str(node) + " With momentum: " + str(momentum))
        movable_locations = get_movable_locations((node.x_cord, node.y_cord), random_order=False, momentum=momentum)
        movable_nodes = convert_locations_to_nodes(movable_locations, node, destination=end, momentum=momentum)
        print("movable_nodes")
        print_node_list(movable_nodes)

        print("visited nodes")
        print_node_list(visited)

        node.momentum = momentum
        visited.append(node)
        for movable_node in movable_nodes:
            if (movable_node.x_cord, movable_node.y_cord) == end:
                visited.append(movable_node)
                return (cost + movable_node.cost, visited)
            
            elif movable_node not in visited:
                node_cost = lambda node_1 : node_1.cost
                enqueued.append(movable_node)
                enqueued.sort(key=node_cost)

def print_map(ski_map):
    for row in ski_map:
        print(row)

def print_node_list(nodes):
    for node in nodes:
        print(str(node) + ";momentum: " + str(node.momentum))

def write_path_to_file(paths):
    f = open("output.txt", "w")
    if paths is None or len(paths) == 0:
        f.write("FAIL")
        return

    for path in paths:
        if len(path) == 0:
            line = "FAIL\n"
        else:
            line = ""
            for node in path:
                line = line + f"{node.x_cord},{node.y_cord} "
            
            line = line + "\n"
        f.write(line)




file = open('input.txt','r')
file_lines = file.readlines()


# Convert read bytes into ints wherever applicable
algorithm = file_lines[0].strip()
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


paths = []

for lodge_loc in lodge_locs:
    if algorithm == "BFS":
        start_node = Node(x=start_x, y=start_y)
        cost, visted_node_list = bfs((lodge_loc[0], lodge_loc[1]), enqueued=[start_node])
        path = trace_to_root(visted_node_list)
        paths.append(path)
    elif algorithm == "UCS":
        start_node = Node(x=start_x, y=start_y)
        cost, visted_node_list = ucs((lodge_loc[0], lodge_loc[1]), enqueued=[start_node])
        path = trace_to_root(visted_node_list)
        paths.append(path)
    elif algorithm == "A*":
        start_node = Node(x=start_x, y=start_y)
        cost, visted_node_list = a_star((lodge_loc[0], lodge_loc[1]), enqueued=[start_node])
        path = trace_to_root(visted_node_list)
        paths.append(path)


write_path_to_file(paths)