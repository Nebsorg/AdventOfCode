from datetime import datetime
import copy
import sys
import re

sys.setrecursionlimit(100000000)

#### Main
print("2023 --- Day 10: Pipe Maze ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    maze = {}
    max_row = -1 
    for i, line in enumerate(f):
        line = line.rstrip()

        if i == 0:
            max_col = len(line)-1

        for j, char in enumerate(line):
            maze[(i,j)] = char
            if char == 'S':
                start = (i,j)
   
        max_row += 1
    return(start, (max_row, max_col, maze))

def isConnected(p1, p2, maze):
    CONNECTION_DOWN_TO_UP = ['J', '|', 'L']
    CONNECTION_UP_TO_DOWN = ['7', '|', 'F']
    
    CONNECTION_RIGHT_TO_LEFT = ['J', '-', '7']
    CONNECTION_LEFT_TO_RIGHT = ['F', '-', 'L']

    if maze[p1] == '.' or maze[p2] == '.':
        return(False)

    ## get p2 position from p2 : 
    if p1[0] == p2[0]:
        if p1[1]+1 == p2[1]:
            if maze[p1] in CONNECTION_LEFT_TO_RIGHT and maze[p2] in CONNECTION_RIGHT_TO_LEFT:
                return(True)
        elif p1[1]-1 == p2[1]:
            ## p2 is up, direction is right to left
            if maze[p2] in CONNECTION_LEFT_TO_RIGHT and maze[p1] in CONNECTION_RIGHT_TO_LEFT:
                return(True)
        return(False)
    elif p1[1] == p2[1]:
        if p1[0]+1 == p2[0]:
            if maze[p1] in CONNECTION_UP_TO_DOWN and maze[p2] in CONNECTION_DOWN_TO_UP:
                return(True)
        elif p1[0]-1 == p2[0]:
            if maze[p2] in CONNECTION_UP_TO_DOWN and maze[p1] in CONNECTION_DOWN_TO_UP:
                return(True)
        return(False)


def getNext(pos, pos_from, g_maze):
    result = getNeighboor(pos, g_maze)
    return([d for d in result if d!=pos_from])



def getNeighboor(pos, g_maze):
    result = []
    shifts = [(1,0), (-1,0), (0,1), (0,-1)]
    max_row = g_maze[0]
    max_col = g_maze[1]
    maze = g_maze[2]

    for shift in shifts:
        new_pos = (pos[0] + shift[0], pos[1] + shift[1])
        if (0 <= new_pos[0] <= max_row) and (0 <= new_pos[1] <= max_col):
            if isConnected(pos, new_pos, maze):
                result.append(new_pos)
    return(result)


def explore(pos, path, g_maze):
    if pos in path:
        return(path)

    next_positions = getNext(pos, path[-1], g_maze)

    if len(next_positions) == 0:
        return([])
    elif len(next_positions) == 1:
        updated_path = list(path)
        updated_path.append(pos)
        return(explore(next_positions[0], updated_path, g_maze))
    else:
        return([])


def isInside(pos, g_maze, path):
    max_row = g_maze[0]
    max_col = g_maze[1]
    maze = g_maze[2]
    
    
    if pos in path:
        ## fait partie du chemin, il n'est pas à l'interieur
        return(False) 

    ## un element est à l'interieur si le nombre de frontiere qu'il croise dans une direction est impair
    ## seul les point horizontaux et verical sont priss
    shifts = [(1,0), (-1,0), (0,1), (0,-1)]
    regexps_shift = [["(F\|*J)", "-", "(7\|*L)"],
                     ["(L\|*7)", "-", "(J\|*F)"],
                     ["(L-*7)", "\|", "(F-*J)"],
                     ["(J-*F)", "\|", "(7-*L)"]]
    
    for i, shift in enumerate(shifts):
        frontiers = ""
        new_pos = (pos[0] + shift[0], pos[1] + shift[1])
        while (0 <= new_pos[0] <= max_row) and (0 <= new_pos[1] <= max_col):
            if new_pos in path:
                frontiers+=maze[new_pos]
            new_pos = (new_pos[0] + shift[0], new_pos[1] + shift[1])

        regexps = regexps_shift[i]
        border_crossed = 0
        for reg_exp in regexps:
            result = re.findall(reg_exp, frontiers)
            border_crossed += len(result)

        if border_crossed%2==0:
            return(False)
    return(True)




def countInside(g_maze, loop):
    maze = g_maze[2]

    inside = []
    for pos in maze.keys():
        if isInside(pos, g_maze, loop):
            inside.append(pos)

    print(f"****** Second Star = {len(inside)}")


def FirstStar(start, g_maze):
    maze = g_maze[2]
    ##exploring : 
    print(f"INIT Exploring from position {start} = {maze[start]}")
    
    ## trying all the pipe possible for start : 
    for start_pipe in ['7','|', '-', 'F', 'L', 'J']:
        print(f"Remplacing Start pipe by {start_pipe}")
        current_g_maze = copy.deepcopy(g_maze)
        current_g_maze[2][start] = start_pipe
        
        ## starting
        next_positions = getNeighboor(start, current_g_maze)
        
        for next_position in next_positions:
            path = [start]
            result = explore(next_position, path, current_g_maze)
            if len(result) > 1: 
                ## loop found !
                print(f"Start pipe = {start_pipe} --> loop found of length {len(result)}")
                return(result)
            else:
                print(f"Start pipe = {start_pipe} --> no loop found")
    return([])
    
    

fileToOpen = "./2023/Day10.txt"
start, g_maze = readInstruction(fileToOpen)

loop = FirstStar(start, g_maze)
print(f"****** First Star = {len(loop)//2}")

countInside(g_maze,loop)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 