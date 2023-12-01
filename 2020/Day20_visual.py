import os
import sys
import pygame
from datetime import datetime
import copy
import time
import math

HORIZONTAL = 0
VERTICAL = 1
TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3


windowsWidth = 960
windowsHeight = 960

def compareEdges(edge1, edge2):
    if len(edge1) != len(edge2):
        return(0)

    size = len(edge1)
    ## testing if equal
    for i, val in enumerate(edge1):
        if val != edge2[i]:
            break
    else:
        return(1) ## equal

    ## testing if equal flipped
    for i, val in enumerate(edge1):
        if val != edge2[size-i-1]:
            break
    else:
        return(2) ## equal flipped
    return(0)


def getEdges(img):
    edges = []
    edges.append(img[0]) ## top
    edges.append(img[len(img)-1]) ## bottom
    colFirst = []
    colLast = []
    for i, line in enumerate(img):
        colFirst.append(line[0])
        colLast.append(line[len(line)-1])
    edges.append(colFirst)
    edges.append(colLast)
    return(edges)

## return list of tile which have an edge which match
## returning (ID = id of the matchinf tile,
##            posTile = which edge is matching on the current tile : up, down, left or right
##            posMatchingTile = which edge is matching on the matching tile : up, down, left or right
##            matching = type of matching : 1 = straight / 2 = flipped
def getMatchTile(refId, tileList):
    result = []
    edgesSource = getEdges(tileList[refId])
    for id, img in tileList.items():
        if id == refId:
            continue
        else:
            edgesDest = getEdges(img)
            for posTile, edgeSource in enumerate(edgesSource):
                for posMatching, edgeDest in enumerate(edgesDest):
                    matching = compareEdges(edgeSource, edgeDest)
                    if matching > 0:
                        result.append((id, posTile, posMatching, matching))
                        break
    return(result)

def drawLayout(puzzleShape, pictures, screen):
    ## spliting the screen to display layout
    currentPuzzle = next(iter(pictures.values()))
    xShift = windowsWidth / (len(currentPuzzle)*len(puzzleShape))
    yShift = windowsHeight / (len(currentPuzzle[0])*len(puzzleShape[0]))
    xPuzzleShift = int(xShift * len(currentPuzzle))
    yPuzzleShift = int(yShift * len(currentPuzzle[0]))
    xShift = int(xShift)
    yShift = int(yShift)

    for i in range(len(puzzleShape)):
        for j in range(len(puzzleShape[0])):
            puzzleID = puzzleShape[i][j]
            if puzzleID == -1:
                color = (127,127,127)
                xPos = j*xPuzzleShift
                yPos = i*yPuzzleShift
                pygame.draw.rect(screen, color, (xPos, yPos, xPuzzleShift, yPuzzleShift))
            else:
                currentPuzzle = pictures[puzzleShape[i][j]]

                for y in range(len(currentPuzzle)):
                    for x in range(len(currentPuzzle[0])):
                        xPos = x*xShift + j*xPuzzleShift
                        yPos = y*yShift + i*yPuzzleShift
                        if currentPuzzle[y][x] == '.':
                            color = (10,14,255)
                        elif currentPuzzle[y][x] == '#':
                            color = (255,255,255)
                        pygame.draw.rect(screen, color, (xPos, yPos, xShift, yShift))
    ## drawing separation line
    color = (0,255,0)
    for i in range(len(puzzleShape)):
        pygame.draw.line(screen, color, (0,i*yPuzzleShift), (windowsWidth,i*yPuzzleShift))
        pygame.draw.line(screen, color, (i*xPuzzleShift,0), (i*xPuzzleShift, windowsHeight))

    pygame.display.flip()
    pygame.event.pump()

def drawBigPicture(bigPicture, screen):
    xShift = windowsWidth / len(bigPicture)
    yShift = windowsHeight / len(bigPicture[0])

    for i in range(len(bigPicture)):
        for j in range(len(bigPicture[0])):
                xPos = j*xShift
                yPos = i*yShift
                if bigPicture[i][j] == '.':
                    color = (10,14,255)
                elif bigPicture[i][j] == '#':
                    color = (255,255,255)
                else:
                    color = (255,33,77)
                pygame.draw.rect(screen, color, (xPos, yPos, xShift, yShift))
    pygame.display.flip()
    pygame.event.pump()


def getDatas():
    tileList = {}
    currentImg = []
    tileId = -1
    readingTile = False
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day20.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if readingTile:
            if line == "":
                ## image completed
                tileList[tileId] = currentImg
                readingTile = False
            else:
                currentImg.append(list(line))
        else:
            if ':' in line:
                tileId = int(line[5:9])
                readingTile = True
                currentImg = []
    f.close()

    print(f"Nb Tile = {len(tileList)} - tile ID : {tileList.keys()}")

    matchList = {}
    star1 = 1
    for id in tileList:
        matchList[id] = getMatchTile(id, tileList)
        if len(matchList[id]) == 2:
            star1 *= id
    print(f"matchList:{matchList}")

    print(f"Star1: {star1}")

    ### constucting full image with random allocation of tile
    keyList = list(tileList.keys())
    gridSize = int(math.sqrt(len(tileList)))
    fullImage = []
    for i in range(gridSize):
        line = []
        for j in range(gridSize):
            line.append(keyList[i*gridSize+j])
        fullImage.append(line)
    print(f"FullImage = {fullImage}")
    return(fullImage, tileList, matchList)

def flip(image, symetrie):
    if symetrie == HORIZONTAL:
        for i in range(int(len(image)/2)):
            line = image[i].copy()
            image[i] = image[len(image)-i-1].copy()
            image[len(image)-i-1] = line
    else:
        for j in range(int(len(image)/2)):
            for i in range(len(image)):
                temp = image[i][j]
                image[i][j] = image[i][len(image)-j-1]
                image[i][len(image)-j-1] = temp

def flipDiagonal(image):
    for i in range(len(image)):
        for j in range(i, len(image[0])):
            if i == j:
                continue
            temp = image[i][j]
            image[i][j] = image[j][i]
            image[j][i] = temp

def rotate(image):
    flipDiagonal(image)
    flip(image, VERTICAL)

## return in order TOP, BOTTOM, LEFT, RIGHT
def getNeigborsCoordinate(i,j, max):
    neighbors = []
    vector = [(-1,0), (1,0), (0,-1), (0,1)]

    for shift in vector:
        pos_i = i + shift[0]
        pos_j = j + shift[1]
        if 0 <= pos_i < max and 0<= pos_j < max:
            neighbors.append((pos_i, pos_j))
        else:
            neighbors.append(None)
    return(neighbors)


def makeItMatches(edgeToMatch, direction, id, pictures):
    ##rotating & flipping the img to have the direction edge matching the edgetoMatch straight
    img = pictures[id]
    ## trying to rotate it 3 times to see if it can matches
    for n in range(4):
        edge = getEdges(img)[direction]
        comparison = compareEdges(edgeToMatch, edge)
        if comparison > 0:
            ## edge matching. Flipping it if needed
            if comparison == 2:
                if direction == TOP or direction == BOTTOM:
                    flip(img, VERTICAL)
                else:
                    flip(img, HORIZONTAL)
            return(True)
        rotate(img)
    return(False)

def PlaceTile(puzzleShape, pictures, matchList, screen):
    ## reinitializing puzzleShapre
    for i in range(len(puzzleShape)):
        for j in range(len(puzzleShape[0])):
            puzzleShape[i][j] = -1

    drawLayout(puzzleShape, pictures, screen)
    ## selecting first element on top left with borders

    for id, matches in matchList.items():
        if len(matches) == 2:
            if (matches[0][1] == BOTTOM and matches[1][1] == RIGHT) or (matches[0][1] == RIGHT and matches[1][1] == BOTTOM):
                puzzleShape[0][0] = id
    drawLayout(puzzleShape, pictures, screen)
    print(printMatrix(puzzleShape))

    pieceInPlace = 1
    iteration = 0
    target = len(puzzleShape)**2
    ## solving the puzzle starting from 0,0
    while pieceInPlace < target and iteration < 50:
        for i_slot in range(len(puzzleShape)):
            for j_slot in range(len(puzzleShape[0])):
                currentSlot = puzzleShape[i_slot][j_slot]
                print(f"#{iteration} - treating slot {i_slot,j_slot} = {currentSlot} ")
                if currentSlot != -1:
                    neighbors = getNeigborsCoordinate(i_slot, j_slot, len(puzzleShape))
                    for relativePosition, coordinate in enumerate(neighbors):
                        if coordinate != None:
                            if puzzleShape[coordinate[0]][coordinate[1]] == -1:
                                ##no tile position for this neigboirs relativePosition
                                potentials = matchList[currentSlot]
                                if relativePosition == TOP:
                                    ## trying to fill the tile on top of this tileId
                                    print(f"#{iteration} - tile on TOP of {i_slot,j_slot, currentSlot} is empty - looking for matching tile - candidate: {potentials}")
                                    edgeToMatch = getEdges(pictures[currentSlot])[TOP]
                                    directionToMatch = BOTTOM
                                elif relativePosition == BOTTOM:
                                    ## trying to fill the tile on top of this tileId
                                    print(f"#{iteration} - tile on BOTTOM of {i_slot,j_slot, currentSlot} is empty - looking for matching tile - candidate: {potentials}")
                                    edgeToMatch = getEdges(pictures[currentSlot])[BOTTOM]
                                    directionToMatch = TOP
                                elif relativePosition == RIGHT:
                                    ## trying to fill the tile on top of this tileId
                                    print(f"#{iteration} - tile on RIGHT of {i_slot,j_slot, currentSlot} is empty - looking for matching tile - candidate: {potentials}")
                                    edgeToMatch = getEdges(pictures[currentSlot])[RIGHT]
                                    directionToMatch = LEFT
                                else:
                                    ## trying to fill the tile on top of this tileId
                                    print(f"#{iteration} - tile on LEFT of {i_slot,j_slot, currentSlot} is empty - looking for matching tile - candidate: {potentials}")
                                    edgeToMatch = getEdges(pictures[currentSlot])[LEFT]
                                    directionToMatch = RIGHT

                                print(f"#{iteration} - edge to match = {edgeToMatch} - direcion={directionToMatch}")
                                for tryMatch in potentials:
                                    print(f"#{iteration} - testing {tryMatch[0]}")
                                    if makeItMatches(edgeToMatch, directionToMatch, tryMatch[0], pictures):
                                        puzzleShape[coordinate[0]][coordinate[1]] = tryMatch[0]
                                        time.sleep(0.05)
                                        drawLayout(puzzleShape, pictures, screen)
                                        pieceInPlace += 1
                                        break;

                drawLayout(puzzleShape, pictures, screen)
                print(printMatrix(puzzleShape))

                    ## trying to fill neighbors :
        iteration += 1
        if pieceInPlace == target:
            return(True)
        else:
            return(False)


def createBigPicture(puzzleShape, pictures):
    removeExteriorLines(pictures)

    firstPicture = next(iter(pictures.values()))
    row_shift = len(firstPicture)
    col_shift = len(firstPicture[0])
    nb_row = row_shift*len(puzzleShape)
    nb_col = col_shift*len(puzzleShape[0])

    bigPicture = [(['x']*nb_col) for i in range(nb_row)]
    for i in range(len(puzzleShape)):
        for j in range(len(puzzleShape[0])):
            img = pictures[puzzleShape[i][j]]
            for inner_i in range(len(img)):
                for inner_j in range(len(img[0])):
                    bigPicture[i*row_shift+inner_i][j*col_shift+inner_j] = img[inner_i][inner_j]
    return(bigPicture)

def detectSeaMonster(i,j, bigPicture, action):
    patern = [(1,1),(0,3),(-1,1),(0,1),(1,1),(0,3),(-1,1),(0,1),(1,1),(0,3),(-1,1),(0,1),(-1,0),(1,1)]
    #patern = [(0,1),(-1,1),(1,1)]
    #patern = [(-2,0),(0,1),(1,0),(0,1),(1,0)]
    #patern = [(1,1),(0,1),(0,1),(-1,0),(0,1), (1,1), (0,1), (0,1), (1,0), (0,1), (0,1), (-1,0)]

    if action == 1:
        bigPicture[i][j] = 'X'

    current_i = i
    current_j = j
    for shift in patern:
        current_i += shift[0]
        current_j += shift[1]

        if 0 <= current_i < len(bigPicture) and 0 <= current_j < len(bigPicture[0]):
            if bigPicture[current_i][current_j] == '#':
                if action == 1:
                    bigPicture[current_i][current_j] = 'X'
                continue
            else:
                return(False)
        else:
            return(False)
    return(True)



def searchSeaMonster(bigPicture, screen):
    nbOfSeaMonster = 0
    for i in range(len(bigPicture)):
        for j in range(len(bigPicture[0])):
            value = bigPicture[i][j]
            if value == '#':
                if detectSeaMonster(i, j, bigPicture, 0):
                    nbOfSeaMonster += 1
                    detectSeaMonster(i, j, bigPicture, 1)
                    drawBigPicture(bigPicture, screen)
                    time.sleep(0.2)
    return(nbOfSeaMonster)

def parseSeaMonster(bigPicture, screen):
    ## operation à tester :
    # 1 - direct
    # 2 - flip hori
    # 3 - flip verti
    # 4 - flip hori puis flip verti
    # on fait une rotation et on recommence

    for i in range(4):
        numberOfSeaMonster = searchSeaMonster(bigPicture, screen)
        if numberOfSeaMonster > 0:
            return(numberOfSeaMonster)

        testPicture = bigPicture.copy()
        flip(testPicture, HORIZONTAL)
        drawBigPicture(testPicture, screen)
        time.sleep(0.5)
        numberOfSeaMonster = searchSeaMonster(testPicture, screen)
        if numberOfSeaMonster > 0:
            return(numberOfSeaMonster)

        testPicture = bigPicture.copy()
        flip(testPicture, VERTICAL)
        drawBigPicture(testPicture, screen)
        time.sleep(0.5)
        numberOfSeaMonster = searchSeaMonster(testPicture, screen)
        if numberOfSeaMonster > 0:
            return(numberOfSeaMonster)

        testPicture = bigPicture.copy()
        flip(testPicture, VERTICAL)
        flip(testPicture, HORIZONTAL)
        drawBigPicture(testPicture, screen)
        time.sleep(0.5)
        numberOfSeaMonster = searchSeaMonster(testPicture, screen)
        if numberOfSeaMonster > 0:
            return(numberOfSeaMonster)

        testPicture = bigPicture.copy()
        flip(testPicture, HORIZONTAL)
        flip(testPicture, VERTICAL)
        drawBigPicture(testPicture, screen)
        time.sleep(0.5)
        numberOfSeaMonster = searchSeaMonster(testPicture, screen)
        if numberOfSeaMonster > 0:
            return(numberOfSeaMonster)

        rotate(bigPicture)
        drawBigPicture(bigPicture, screen)
        time.sleep(0.5)
    return(0)

def removeExteriorLines(pictures):
    for key in pictures.keys():
        img = pictures[key]
        newImage = []
        for i, line in enumerate(img):
            if i > 0 and i < len(line)-1:
                newImage.append(line[1:-1])
        pictures[key] = newImage

def getRoughness(bigpictures):
    roughness = 0
    for i in range(len(bigpictures)):
        for j in range(len(bigpictures[0])):
            if bigpictures[i][j] == '#':
                roughness += 1
    return(roughness)

def main():

    # initialize the pygame module
    pygame.init()
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("Advent Of Code - Day 20 - random placement")

    # create a surface on screen
    screen = pygame.display.set_mode((windowsWidth,windowsHeight))

    puzzleShape, pictures, matchList = getDatas()
    drawLayout(puzzleShape, pictures, screen)
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
                    pygame.display.set_caption("Advent Of Code - Day 20 - Constructing the image")

                    if PlaceTile(puzzleShape, pictures, matchList, screen):
                        print(f"All tile positionned - searching for snakes")
                        pygame.display.set_caption("Advent Of Code - Day 20 - Creating Big Picture")
                        pygame.event.clear()
                        ## creating the big picture :
                        time.sleep(1)
                        bigPicture = createBigPicture(puzzleShape, pictures)
                        drawBigPicture(bigPicture, screen)
                        time.sleep(1)

                        pygame.display.set_caption("Advent Of Code - Day 20 - searching for sea monsters !")
                        pygame.event.clear()

                        ## Searching for sea monster !
                        numberOfSeaMonster = 0
                        numberOfSeaMonster = parseSeaMonster(bigPicture, screen)
                        roughness = getRoughness(bigPicture)
                        print(f"Advent Of Code - Day 20 - {numberOfSeaMonster} Sea Monster found ! roughness (star2) = {roughness}")
                        pygame.display.set_caption(f"Advent Of Code - Day 20 - {numberOfSeaMonster} Sea Monster found ! roughness (star2) = {roughness}")
                        pygame.event.clear()



                if event.key == pygame.K_DOWN:
                    print(printMatrix(puzzleShape))
                    bigPicture = createBigPicture(puzzleShape, pictures)
                    drawBigPicture(bigPicture, screen)


def printMatrix(mat):
    result = ""
    for i in range(len(mat)):
        result += ' '.join(str(mat[i])) + '\n'
    return(result)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    start_time = datetime.now()
    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    main()

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
