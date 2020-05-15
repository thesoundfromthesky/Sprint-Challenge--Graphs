from room import Room
from player import Player
from world import World
from math import inf
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

#random start
# world.staring_room = random.choice(world.rooms)

#starts at 0
player = Player(world.starting_room)


# Fill this out with directions to walk
traversal_path = []

def tp_push(v):
    traversal_path.append(v)

#graphs
g={}

#reverse directions
r_d={"n":"s", "s":"n", "w":"e", "e":"w"}

#queue
q=[]
def eq(e):
    q.insert(0, e)
def dq():
    return q.pop()

#stack
s=[]
def push(e):
    s.append(e)
def pop():
    return s.pop()

# to add room to graphs
def a_r(r):
    r_id = r.id
    g[r_id]={}
    exits=r.get_exits()
    for i in exits:
        g[r_id][i]="?"

def is_r_in_g(r):
    if r.id not in g:
        a_r(r)

def log(d):
    player.travel(d)
    tp_push(d)

starting_room = player.current_room

def recur(r):
    is_r_in_g(r)
    exits= r.get_exits()
    #comment to remove randomness
    random.shuffle(exits)
    for i in exits:
        if g[r.id][i] != "?":
            continue

        #move player and log
        log(i)

        #get move room id 
        r_id = player.current_room.id
        is_r_in_g(player.current_room)
        #update g direction with moved room id        
        g[r.id][i]=r_id

        # get reversed direction
        d = r_d[i]
        #update g with previous room id
        g[r_id][d]=r.id

        recur(player.current_room)

        if len(g) == len(room_graph):
            return

        log(d)

recur(starting_room)

# best: 968 
goal = 984
while len(traversal_path) > goal:
    player.current_room = world.starting_room
    traversal_path = []
    g={}
    recur(player.current_room)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
