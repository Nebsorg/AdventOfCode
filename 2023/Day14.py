from datetime import datetime
import copy
from tools import Style

#### Main
print(f"{Style.RED}2023 --- Day 14: Parabolic Reflector Dish ---{Style.RESET}")
start_time = datetime.now()

def getLine(pattern, line_id):
    if 0 <= line_id < len(pattern):
        return(pattern[line_id])
    else:
        return([])

def getColumn(pattern, col_id):
    if 0 <= col_id < len(pattern[0]):
        result = []
        for i in range(len(pattern)):
            result.append(pattern[i][col_id])
        return(result)
    else:
        return([])

def display(dish):
    for i in range(len(dish)):
        line = ''.join(dish[i])
        print(line)
        

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    dish = []
    for line in f:
        line = line.rstrip()
        dish.append(list(line))
    return(dish)

def collapse(vector):
    empty_space = 0
    stop_position = -1
    new_vector = copy.deepcopy(vector)
    i = 0
    while i < len(vector):
        val = new_vector[i]

        if val == '.':
            #print(f"{i}={val} -- Empty Space -- continue {empty_space}- {new_vector}")
            empty_space += 1
            i += 1
            continue

        if val == '#':
            #print(f"{i}={val} -- Rock -- reset {stop_position} - {new_vector}")
            stop_position = i
            empty_space = 0
            i+=1
            continue

        if val == 'O':
            #print(f"{i}={val} -- round - shift {stop_position}- {new_vector}")
            if empty_space > 0:
                new_vector[stop_position+1] = 'O'
                new_vector[i] = '.'
                empty_space = 0
                stop_position += 1
                i = stop_position+1
            else:
                stop_position = i
                empty_space = 0
                i += 1
    return(new_vector)

def tiltEast(map):
    tilted = []
    for i in range(len(map)):
        line = getLine(map, i)
        line.reverse()
        new_line = collapse(line)
        new_line.reverse()
        tilted.append(new_line)
    return(tilted)


def tiltWest(map):
    tilted = []
    for i in range(len(map)):
        line = getLine(map, i)
        new_line = collapse(line)
        tilted.append(new_line)
    return(tilted)

def tiltNorth(map):
    tilted = []
    for j in range(len(map[0])):
        column = getColumn(map, j)
        new_col = collapse(column)
        for i in range(len(new_col)):
            if j == 0:
                tilted.append([new_col[i]])
            else:
                tilted[i].append(new_col[i])
    return(tilted)

def tiltSouth(map):
    tilted = []
    for j in range(len(map[0])):
        column = getColumn(map, j)
        column.reverse()
        new_col = collapse(column)
        new_col.reverse()
        for i in range(len(new_col)):
            if j == 0:
                tilted.append([new_col[i]])
            else:
                tilted[i].append(new_col[i])
    return(tilted)

def evaluate(map):
    result = 0
    for i in range(len(map)):
        result += map[i].count('O')*(len(map)-i)
    return(result)

def stars(dish):
    star1 = 0
    star2 = 0

    cyclesNb = 1000000000

    history = []
    tiltedEast = copy.deepcopy(dish)
    history.append(copy.deepcopy(tiltedEast))
    cylceid = 1
    loopFound = False
    while cylceid <= cyclesNb:
        tiltedNorth = tiltNorth(tiltedEast)
        if cylceid == 1:
            star1 = evaluate(tiltedNorth)
            print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")
        
        tiltedWest = tiltWest(tiltedNorth)
        tiltedSouth = tiltSouth(tiltedWest)
        tiltedEast = tiltEast(tiltedSouth)

        if not loopFound:
            if tiltedEast in history:
                startLoopId = history.index(tiltedEast)+1
                loopsize = cylceid - startLoopId + 1
                print(f"Loop Found on cycle {cylceid} in position {startLoopId} -- loop size = {loopsize}")
                cylceid = cyclesNb - (cyclesNb-cylceid)%loopsize +1
                loopFound = True
            else:
                history.append(copy.deepcopy(tiltedEast))
                cylceid += 1
        else:
            cylceid += 1        


    star2 = evaluate(tiltedEast)
    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day14.txt"
dish = readInstruction(fileToOpen)

stars(dish)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 