import os
import sys
import pygame
from datetime import datetime
import copy
import time

windowsWidth = 1000
windowsHeight = 1000

def countOccupiedSeat(layout):
    count = 0
    for line in layout:
        count += line.count('#')
    return(count)

def getNbSeatOccupiedAroundNear(pos, layout):
    count = 0
    vecteurs = [(1,0), (1,-1), (1,1), (-1,0), (-1,1), (-1,-1), (0,-1), (0, 1)]

    for vecteur in vecteurs:
        testX = pos[0] + vecteur[0]
        testY = pos[1] + vecteur[1]
        if (0 <= testX < len(layout)) and (0 <= testY < len(layout[0])):
            if layout[testX][testY] == '#':
                count += 1
    return(count)

def getNbSeatOccupiedAroundFar(pos, layout):
    count = 0
    vecteurs = [(1,0), (1,-1), (1,1), (-1,0), (-1,1), (-1,-1), (0,-1), (0, 1)]

    for vecteur in vecteurs:
        testX = pos[0] + vecteur[0]
        testY = pos[1] + vecteur[1]
        while (0 <= testX < len(layout)) and (0 <= testY < len(layout[0])):
            if layout[testX][testY] == '.':
                testX += vecteur[0]
                testY += vecteur[1]
            elif layout[testX][testY] == '#':
                count += 1
                break
            else:
                break
    return(count)

def star1(layout, screen):
    stabilized = False
    iteration = 1
    while not stabilized:
        newLayout = copy.deepcopy(layout)
        for x in range(len(layout)):
            for y in range(len(layout[0])):
                nbOccupied = getNbSeatOccupiedAroundNear((x,y), layout)
                if (layout[x][y] == "L") and (nbOccupied == 0):
                    newLayout[x][y] = '#'
                elif (layout[x][y] == "#") and (nbOccupied >= 4):
                    newLayout[x][y] = 'L'
        if newLayout == layout:
            stabilized = True
        else:
            layout = newLayout
            iteration +=1
        time.sleep(.100)
        drawLayout(layout, screen)
    return(countOccupiedSeat(layout), iteration)

def star2(layout, screen):
    stabilized = False
    iteration = 1
    while not stabilized:
        newLayout = copy.deepcopy(layout)
        for x in range(len(layout)):
            for y in range(len(layout[0])):
                nbOccupied = getNbSeatOccupiedAroundFar((x,y), layout)
                if (layout[x][y] == "L") and (nbOccupied == 0):
                    newLayout[x][y] = '#'
                elif (layout[x][y] == "#") and (nbOccupied >= 5):
                    newLayout[x][y] = 'L'
        if newLayout == layout:
            stabilized = True
        else:
            layout = newLayout
            iteration +=1
        time.sleep(.100)
        drawLayout(layout, screen)
    return(countOccupiedSeat(layout), iteration)

def drawLayout(layout, screen):
    ## spliting the screen to display layout
    xShift = windowsWidth / len(layout)
    yShift = windowsHeight / len(layout[0])
    for x in range(len(layout)):
        for y in range(len(layout[0])):
            if layout[x][y] == '.':
                color = (0,0,0)
            elif layout[x][y] == '#':
                color = (255,0,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(screen, color, (x * xShift, y * yShift, xShift, yShift))
    pygame.display.flip()

def getLayout():
    layout = []
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day11.txt", "r")
    for line in f:
         layout.append(list(line.rstrip("\n")))
    f.close()
    return(layout)

# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load(directoryPath+"/logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("Advent Of Code - Day 11 - Star 2")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((windowsWidth,windowsHeight))

    layout = getLayout()
    drawLayout(layout, screen)


    #result, iteration = star2(layout, screen)
    #print(f"star2: {result} ({iteration} iteration)")

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
                result, iteration = star2(layout, screen)
                print(f"star2: {result} ({iteration} iteration)")
                pygame.display.set_caption(f"Advent Of Code - Day 11 - Star 2: {result} ({iteration} iteration)")



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    main()
