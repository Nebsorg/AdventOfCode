import os
import pygame
from datetime import datetime
from datetime import datetime
from collections import defaultdict
from operator import mul
from functools import reduce
import re
import copy
import numpy as np


#### Global Variable
g_global_robot_size = 8
g_largeur_fenetre = 1440
g_hauteur_fenetre = 960

g_color_grey = (127,127,127)
g_color_black = (0,0,0)
g_color_green = (0,255,0)

def render(robots):
    ## draw background
    color = g_color_black
    pygame.draw.rect(g_screen, color, (0, 0, g_largeur_fenetre, g_hauteur_fenetre))

    color = g_color_green
    for robot in robots.values():
        pygame.draw.rect(g_screen, color, (robot[0]*g_global_robot_size, robot[1]*g_global_robot_size, g_global_robot_size, g_global_robot_size))
    
    pygame.display.flip()
    pygame.event.pump()

def main(histories):
    global g_screen
    global g_board
    global g_pos_x, g_pos_y

    max_x = histories[0]
    max_y = histories[1]
    history = histories[2]
    candidates = histories[3]
    christmas_tree = candidates[0]

    g_largeur_fenetre = max_x * g_global_robot_size
    g_hauteur_fenetre = max_y * g_global_robot_size
    timeframes = history.keys()


    # initialize the pygame module
    pygame.init()
    #pygame.display.set_icon(logo)
    pygame.display.set_caption(f"Day 14: Restroom Redoubt --- {max_x}, {max_y}")

    # create a surface on screen
    g_screen = pygame.display.set_mode((g_largeur_fenetre, g_hauteur_fenetre))
    timeframe = -1

    #display(max_x, max_y, history[timeframe])

    running = True
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            ## print(f"On a un event {event}")
            if event.type == pygame.MOUSEBUTTONUP:
                print(f"Mouse UP")

            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    timeframe -= 1
                if event.key == pygame.K_RIGHT:
                    timeframe += 1
                if event.key == pygame.K_UP:
                    timeframe -= 100
                if event.key == pygame.K_DOWN:
                    timeframe += 100
                if event.key == pygame.K_PAGEDOWN:
                    timeframe += 1000
                if event.key == pygame.K_PAGEUP:
                    timeframe -= 1000
                print(timeframe)

            pygame.event.clear()

        render(history[timeframe])


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
    regexp = "-?\d+"

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
    history = {}
    candidates = []

    history[-1] = copy.deepcopy(robots)

    for i in range(max_x*max_y):
        for robot in robots.values():
            moveRobot(max_x, max_y, robot)
        if searchTree(robots):
            candidates.append(i+1)
            display(max_x, max_y, robots)
        history[i] = copy.deepcopy(robots)
            #print(f"{i+1} seconds : {robot}")
            #display(max_x, max_y, robots)

    quadrants = evaluate(max_x, max_y, robots)
    print(quadrants)
    star1 = reduce(mul, quadrants)
    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2} - {candidates}")  
    return([max_x, max_y, history, candidates])


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    start_time = datetime.now()
    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)
    print(f"2024 --- Day 14: Restroom Redoubt ---")

    fileToOpen = "./Day14.txt"

    instructions = readInstruction(fileToOpen)

    histories = stars(instructions)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    main(histories)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))











