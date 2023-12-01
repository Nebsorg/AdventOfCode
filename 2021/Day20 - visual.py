import os

import copy

from datetime import datetime
from collections import deque
import pygame


g_windowsWidth = 1400
g_windowsHeight = 1400
g_grey_color = (127,127,127)
g_openNode = (55,55,55)
g_closeNode = (175, 175, 175)
g_currentNode = (255,0,0)
g_otherNode = (255,255,255)
g_boardScreenSize = 1400

def render(inputImage):

    ## draw background
    color = g_grey_color
    pygame.draw.rect(g_screen, color, (0, 0, g_windowsWidth, g_windowsHeight))

    xMax = len(inputImage[0])
    yMax = len(inputImage)

    x_shift = int(g_boardScreenSize / xMax)
    y_shift = int(g_boardScreenSize / yMax)

    print(f"Render picture size {xMax, yMax} -- shift {x_shift, y_shift} -- produit={xMax*x_shift}/{g_boardScreenSize} , {yMax*y_shift}/{g_boardScreenSize}")

    for y in range(yMax):
        for x in range(xMax):
            if inputImage[y][x] == '0':
                color = (0,0,0)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(g_screen, color, (x*x_shift, y*y_shift, x_shift, y_shift))

    pygame.display.flip()
    pygame.event.pump()


def enhancePicture(inputImage, enhancementAlgo, extendValue):
    ## start by increase picture size by x element around
    extendBy = 2
    xMax = len(inputImage[0])

    extendedImage = []

    for i in range(5):
        extendedImage.append([extendValue]*(xMax+2*extendBy))
    for line in inputImage:

        extendedImage.append(([extendValue]*extendBy) + line + ([extendValue]*extendBy))
    for i in range(5):
        extendedImage.append([extendValue]*(xMax+2*extendBy))

    ## Enhence extended Image :
    outputImage = []
    shifts = [-1, 0, 1]

    yMax = len(extendedImage)
    xMax = len(extendedImage[0])

    ## constructing output image per pixel
    for y in range(yMax):
        currentLine = []
        for x in range(xMax):
            index = ''
            for yshift in shifts:
                inputY = y + yshift
                for xshift in shifts:
                    inputX = x + xshift
                    if 0 <= inputX < xMax and 0 <= inputY < yMax:
                        index += extendedImage[inputY][inputX]
                    else:
                        index += extendValue

            ## checking value in algo:
            indexInt = int(index, 2)
            # print(f"  - created index is {index} - {indexInt}  --> {enhancementAlgo[indexInt]}")

            currentLine.append(enhancementAlgo[indexInt])
        outputImage.append(currentLine)
    return (outputImage)


def main():
    global g_screen
    global g_height
    global g_width
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("--- Day 20: Trench Map ---")

    # create a surface on screen
    g_screen = pygame.display.set_mode((g_windowsWidth, g_windowsHeight))
    pygame.font.init()
    global myfont
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    render(inputImage)
    running = True
    # main loop
    path = []
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    extendValue = '0'
                    result = copy.deepcopy(inputImage)
                    for i in range(50):
                        result = enhancePicture(result, enhancementAlgo, extendValue)
                        render(result)
                        if i == 1:
                            brightPoints = sum([v.count('1') for v in result])
                            print(f"** First Star : {brightPoints}")
                        extendValue = enhancementAlgo[int(extendValue * 9, 2)]


                    brightPoints = sum([v.count('1') for v in result])

                    pygame.event.clear()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    print("--- Day 15: Chiton ---")
    #### Main
    start_time = datetime.now()

    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    f = open(".\Day20.txt", "r")
    lineID = 0
    inputImage = []
    for line in f:
        if lineID == 0:
            enhancementAlgo = line.rstrip().replace('#', '1').replace('.', '0')
        elif lineID >= 2:
            inputImage.append(list(line.rstrip().replace('#', '1').replace('.', '0')))
        lineID += 1
    f.close()

    main()

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

