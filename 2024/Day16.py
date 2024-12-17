from datetime import datetime
from collections import defaultdict
from operator import mul
from functools import reduce
import copy
import re
import numpy as np
from collections import deque

#### Main
print(f"2024 --- Day 16: Reindeer Maze ---")
start_time = datetime.now()

regexp = "-?\d+"

def display(start, end, maze, path):
    for i in range(len(maze)):
        line = ""
        for j in range(len(maze[0])):
            if (i,j) in path: line+='O'
            elif (i,j) == start: line+='S'
            elif (i,j) == end: line += 'E'
            else: line+=maze[i][j]
        print(line)

def readInstruction(file):
    f = open(file, "r")
    maze = []

    for i,line in enumerate(f):
        line = line.rstrip()
        maze_line = []
        for j in range(len(line)):
            if line[j] == 'S':
                start = (i,j)
                maze_line.append('.')
            elif line[j] == 'E':
                end = (i,j)
                maze_line.append('.')
            else:
                maze_line.append(line[j])
        maze.append(maze_line)

    return([start, end, maze])


def dijkstraFast(maze, start_pos, direction):

    node_bag = deque([(start_pos, direction)])
    costMap = {(start_pos, direction): [0, set()]}
    max_row = len(maze)
    max_col = len(maze[0])

    while node_bag:
        ## taking a node
        test_node = node_bag.popleft()
        node_pos = test_node[0]
        node_direction = test_node[1]

        ## checking Neighbours
        for shift in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_pos = (node_pos[0] + shift[0], node_pos[1] + shift[1])
            if new_pos[0] < 0 or new_pos[0] >= max_row or new_pos[1] < 0 or new_pos[1] >= max_col:
                continue
            
            if maze[new_pos[0]][new_pos[1]] == '#':
                continue

            if shift == node_direction:
                turn_cost = 0
            elif (node_direction[0]*-1 == shift[0]) and (node_direction[1]*-1 == shift[1]):
                ## 180 degré
                turn_cost = 2000
            else:
                turn_cost = 1000
            
            
            ## updating neighbour cost
            risk = costMap[(node_pos, node_direction)][0] + 1 + turn_cost
            history = copy.deepcopy(costMap[(node_pos, node_direction)][1])
            history.add(node_pos)

            if (new_pos, shift) in costMap:
                if risk < costMap[(new_pos, shift)][0]:
                    ## meilleur chemin, on remplace l'existant
                    costMap[(new_pos, shift)][0] = risk
                    costMap[(new_pos, shift)][1] = history
                    node_bag.append((new_pos, shift))
                elif risk == costMap[(new_pos, shift)][0]:
                    ## chemin equivalent, on ajout ses noeuds à l'historique
                    costMap[(new_pos, shift)][1].update(history)
            else:
                    ## premier pasage, on memorise
                    costMap[(new_pos, shift)] = [risk, history]
                    node_bag.append((new_pos, shift)) 
    return costMap



def stars(instructions):
    star1 = 0
    star2 = 0

    start = instructions[0]
    end = instructions[1]
    maze = instructions[2]

    #display(start, end, maze, [])

    costMap = dijkstraFast(maze, start, (0,1))

    shortestPath = min([(key, val) for key, val in costMap.items() if end == key[0]])
    star1 = shortestPath[1][0]
    star2 = len(shortestPath[1][1])+1

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  

fileToOpen = "./Day16.txt"

instructions = readInstruction(fileToOpen)
#print(instructions)


stars(instructions)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 