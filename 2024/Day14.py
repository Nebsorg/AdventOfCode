from datetime import datetime
from collections import defaultdict
from operator import mul
from functools import reduce
import re
import numpy as np

#### Main
print(f"2024 --- Day 14: Restroom Redoubt ---")
start_time = datetime.now()

regexp = "-?\d+"

def display(max_x, max_y, robots):
    robots_pos = [(r[0], r[1]) for r in robots.values()]
    for y in range(max_y):
        line = ""
        for x in range(max_x):
            if (x,y) in robots_pos: line+='x'
            else: line+='.'
        print('|'+line+'|')
    return(0)

def readInstruction(file):
    f = open(file, "r")
    instructions = []
    robots = {}
    max_x, max_y = 0, 0
    ## read all instruction : 

    for i,line in enumerate(f):
        line = line.rstrip()
        robot = []
        matches = re.finditer(regexp, line)
        for match in matches:
            robot.append(int(match.group()))
        robots[i] = robot
    max_x = max([x[0] for x in robots.values()]) + 1
    max_y = max([x[1] for x in robots.values()]) + 1
    #robots = {}
    #robots[0] = [2,4,2,-3]
    return([(max_x, max_y), robots])

def evaluate(max_x, max_y, robots):

    quadrants = [0,0,0,0]

    for robot in robots.values():
        if 0 <= robot[0] < max_x // 2:
            ## Q1 or Q2
            if 0 <= robot[1] < max_y // 2:
                quadrants[0] += 1
            elif max_y // 2 < robot[1] < max_y:
                quadrants[1] += 1
        elif max_x //2 < robot[0] < max_x:
            ## Q3 or Q4
            if 0 <= robot[1] < max_y // 2:
                quadrants[2] += 1
            elif max_y // 2 < robot[1] < max_y:
                quadrants[3] += 1
    return(quadrants)

def moveRobot(max_x, max_y, robot):
    robot[0] += robot[2]
    robot[1] += robot[3]
    if robot[0] < 0 : robot[0] += max_x
    elif robot[0] >= max_x : robot[0] -= max_x

    if robot[1] < 0 : robot[1] += max_y
    elif robot[1] >= max_y : robot[1] -= max_y

## approche heuristique : si on a plus de 15 robots sur une ligne, et cote à cote, il se passe un truc bizzare, ca doit etre le sapin
def searchTree(robots):
    robots_per_line = defaultdict(lambda : [])
    for robot in robots.values():
        robots_per_line[robot[1]].append(robot)

    for robots_line in robots_per_line.values():
        if len(robots_line) > 15:
            x_pos = set([r[0] for r in robots_line])
            arr = np.array(list(x_pos))
            diff = np.diff(arr)
            is_next = np.all(diff == 1)
            if is_next:
                return(True)
    return(False)

def stars(instructions):
    star1 = 0
    star2 = 0

    max_x = instructions[0][0]
    max_y = instructions[0][1]
    robots = instructions[1]

    display(max_x, max_y, robots)

    ## after max_x*max_y movements, robots are getting back to orinigal state
    for i in range(max_x*max_y):
        for robot in robots.values():
            moveRobot(max_x, max_y, robot)
        if i == 99:
            quadrants = evaluate(max_x, max_y, robots)
            star1 = reduce(mul, quadrants)
        #print(f"{i+1} seconds : {robot}")
        #display(max_x, max_y, robots)

        if searchTree(robots):
            star2 = i+1
            display(max_x, max_y, robots)

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  

fileToOpen = "./Day14.txt"

instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 