from datetime import datetime
import math
import os
import sys
import pygame
import time

windowsWidth = 1000
windowsHeight = 1000

def moveWaypoint(waypoint, value, instruction):
    if instruction == 'N':
        waypoint[1] += value
    elif instruction == 'S':
        waypoint[1] -= value
    elif instruction == 'E':
        waypoint[0] += value
    elif instruction == 'W':
        waypoint[0] -= value
    if instruction == 'R':
        shift = int(value / 90)
        for i in range(shift):
            temp = waypoint[0]
            waypoint[0] = waypoint[1]
            waypoint[1] = -temp
    elif instruction == 'L':
        shift = int(value / 90)
        for i in range(shift):
            temp = waypoint[0]
            waypoint[0] = -waypoint[1]
            waypoint[1] = temp
    return(waypoint)

def drawBoat(screen, boat, position):
    ## spliting the screen to display layout
    screen.blit(boat, [(x / 100)+windowsWidth/2 for x in position])
    pygame.display.flip()
    pygame.event.pump()


def star2(screen):
    boatPosition = [0,0] ## East / North
    waypoint = [10, 1] ## North / East

    boat = pygame.image.load(directoryPath+"/boat_R.png")
    drawBoat(screen, boat, boatPosition)

    f = open("Z:\donnees\developpement\Python\AdventOfCode\day12.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        instruction = line[0]
        value = int(line[1:])

        if instruction == 'F':
            boatPosition[0] += value * waypoint[0]
            boatPosition[1] += value * waypoint[1]
        else:
            waypoint = moveWaypoint(waypoint, value, instruction)
        drawBoat(screen, boat, boatPosition)
    f.close()
    print(f"boatposition= {boatPosition}")
    return(abs(boatPosition[0]) + abs(boatPosition[1]))

def arrow(screen, lcolor, tricolor, start, end, trirad):
    pygame.draw.line(screen,lcolor,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, tricolor, ((end[0]+trirad*math.sin(math.radians(rotation)), end[1]+trirad*math.cos(math.radians(rotation))), (end[0]+trirad*math.sin(math.radians(rotation-120)), end[1]+trirad*math.cos(math.radians(rotation-120))), (end[0]+trirad*math.sin(math.radians(rotation+120)), end[1]+trirad*math.cos(math.radians(rotation+120)))))

def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load(directoryPath+"/logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("Advent Of Code - Day 11")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((windowsWidth,windowsHeight))
    screen.fill((51,110,255))
    pygame.display.update()


    ## solve star 1 visual :
    running = True
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pygame.display.set_caption("Advent Of Code - Day 12 - Star 2")
                    result = star2(screen)
                    print(f"star2: {result}")
                    pygame.display.set_caption(f"Advent Of Code - Day 11 - Star 2: {result}")
                    pygame.event.clear()



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    main()
