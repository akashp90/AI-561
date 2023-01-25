def print_map(ski_map):
	for row in ski_map:
		print(row)


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
	
	print("Counter: ")
	print(counter)
	ski_map_row = file_lines[counter].strip().split(" ")
	ski_map_row = [int(e) for e in ski_map_row]
	print("ski map row")
	print(ski_map_row)
	ski_map.append(ski_map_row)
	counter += 1

print("map")
print_map(ski_map)









































