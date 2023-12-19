from datetime import datetime
import re
from tools import Style
from collections import defaultdict

#### Main
print(f"{Style.RED}2023 --- Day 16: The Floor Will Be Lava ---{Style.RESET}")
start_time = datetime.now()


def display(g_maze, powered_maze):
    max_row = g_maze[0]
    max_col = g_maze[1]
    maze = g_maze[2]

    for i in range(max_row):
        line = ""
        for j in range(max_col):
            if (i,j) in powered_maze.keys():
                line+=str(powered_maze[(i,j)])
            else:
                line += maze[(i,j)]
        print(line)

def readInstruction(file):
    f = open(file, "r")
    maze = {}
    ## read all instruction : 
    for i,line in enumerate(f):
        line = line.rstrip()

        if i == 0:
            max_col = len(line)
        
        for j, val in enumerate(list(line)):
            maze[(i,j)] = val
    return([i+1, max_col, maze])

def evaluateBeam(maze, beam):
    HORIZONTAL_BEAM = [(0,1), (0,-1)]
    VERTICAL_BEAM = [(1,0), (-1,0)]

    powered_maze = defaultdict(lambda: 0)

    lasers = [beam]
    history = []

    while len(lasers) > 0:
        ## testing if current position is in the maze. If not, removing it
        laser = lasers.pop()
        if laser in history:
            ## loop detected --> Killing the beam
            continue

        pos = (laser[0], laser[1])
        direction = (laser[2], laser[3])

        if not(pos in maze.keys()):
            continue

        history.append(laser)
        
        powered_maze[pos] += 1
        action = maze[pos]

        directions = []  
        match action:
            case '.':
                ## keeping the same direction
                directions.append(direction)
            case '-':
                ## if horizontal beam, keeping the same direction
                if direction in HORIZONTAL_BEAM:
                    directions.append(direction)
                else:
                    ##split right and left!
                    directions.append((0, 1))
                    directions.append((0, -1))
            case '|':
                ## if VERTICAL beam, no action : 
                if direction in VERTICAL_BEAM:
                    directions.append(direction)
                else:
                    ##split up and down!
                    directions.append((-1, 0))
                    directions.append((1, 0))
            case '\\':
                    directions.append((direction[1], direction[0]))
            
            case '/':
                    directions.append((-direction[1], -direction[0]))

        ## adding the new position to the lasers: 
        for new_direction in directions:        
            new_laser = (pos[0]+new_direction[0], pos[1]+new_direction[1], new_direction[0], new_direction[1])
            lasers.append(new_laser)

    return(len(powered_maze.keys()))

def stars(g_maze):
    star1 = 0
    star2 = 0

    max_row = g_maze[0]
    max_col = g_maze[1]
    maze = g_maze[2]

    possibles_beams = []

    for i in range(max_row):
        possibles_beams.append((i,0,0,1))
        possibles_beams.append((i,max_col-1,0,-1))

    for i in range(max_col):
        possibles_beams.append((0,i,1,0))
        possibles_beams.append((max_row-1,i,-1,0))
        
    star2 = 0
    for i, beam in enumerate(possibles_beams):
        result = evaluateBeam(maze, beam)
        #print(f"Evaluation of {i+1}/{len(possibles_beams)} : {beam} = {result}")
        star2 = max(result, star2)
        if beam == (0,0,0,1):
            star1 = result

    print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")
    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day16.txt"
g_maze = readInstruction(fileToOpen)

stars(g_maze)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 