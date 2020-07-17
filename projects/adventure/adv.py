from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


def dir_entry(directions_list):
    new_dir = {
        "n": None,
        "e": None,
        "s": None,
        "w": None
    }

    for dir in directions_list:
        new_dir[dir] = dir

    return new_dir

# search of the visited set starting node


def bfs_nearest_open_node(visited, starting_node):
    # create a node que
    node_que = deque()
    node_que.append([starting_node])

    # records the path
    dir_path_que = deque()
    bfs_visited = set()

    # if path is empty, if path empty
    while len(node_que) > 0:
        if len(dir_path_que) <= 0:
            cur_dir_path = []

        # records path
        else:
            cur_dir_path = dir_path_que.popleft()

        cur_node_path = node_que.popleft()
        current_node = cur_node_path[-1]

        bfs_visited.add(current_node.id)

        if len(current_node.get_exits()) > 0:
            for next_node_dir in current_node.get_exits():
                next_node = current_node.get_room_in_direction(next_node_dir)

                if next_node.id not in visited:
                    return [*cur_dir_path, next_node_dir]

                elif next_node.id not in bfs_visited:
                    dir_path_que.append([*cur_dir_path, next_node_dir])
                    node_que.append([*cur_node_path, next_node])

        else:
            print(cur_dir_path)
            return cur_dir_path


traversal_path = []

rms_graph = dict()
visited = set()

while len(visited) < len(world.rooms):
    paths = player.current_room.get_exits()
    room_id = player.current_room.id

    if room_id not in visited:
        visited.add(room_id)

    if room_id not in rms_graph:
        rms_graph[room_id] = dir_entry(paths)

        for next_room in paths:
            rms_graph[room_id][next_room] = player.current_room.get_room_in_direction(
                next_room).id

    unexplored_route = None

    for dir in rms_graph[room_id]:
        if rms_graph[room_id][dir] is not None and rms_graph[room_id][dir] not in visited:
            unexplored_route = dir

    if unexplored_route is not None:
        traversal_path.append(unexplored_route)
        player.travel(unexplored_route)

    else:
        pathfinding = bfs_nearest_open_node(visited, player.current_room)

        if pathfinding is not None:
            for dir in pathfinding:
                print(dir)
                traversal_path.append(dir)
                player.travel(dir)
                visited.add(player.current_room.id)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#
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
