from datetime import datetime
import copy
import re

X = 0
Y = 1
WHITE = 1
BLACK = -WHITE

def star1(hands):
        return(0)


def star2(hands):
    return(0)

def move(coord, direction):
    if direction == 'e':
        return((coord[X], coord[Y]+1))
    elif direction == 'w':
        return((coord[X], coord[Y]-1))
    elif direction == 'ne':
        if coord[X]%2 == 0:
            return((coord[X]-1, coord[Y]+1))
        else:
            return((coord[X]-1, coord[Y]))
    elif direction == 'nw':
        if coord[X]%2 == 0:
            return((coord[X]-1, coord[Y]))
        else:
            return((coord[X]-1, coord[Y]-1))
    elif direction == 'se':
        if coord[X]%2 == 0:
            return((coord[X]+1, coord[Y]+1))
        else:
            return((coord[X]+1, coord[Y]))
    elif direction == 'sw':
        if coord[X]%2 == 0:
            return((coord[X]+1, coord[Y]))
        else:
            return((coord[X]+1, coord[Y]-1))
    else:
        print(f"------- move error : unknown direction {coord}--------- ")
        return(coord)

def countBlack(tilesList):
    total = 0
    for color in tilesList.values():
        if color == BLACK:
            total += 1
    return(total)

def getneighborsCoordinates(coord):
    neighbors = set()
    directions = ['ne', 'nw', 'e', 'se', 'sw', 'w']
    for direction in directions:
        neighbors.add(move(coord, direction))
    return(neighbors)

def getNumberOfBlacktileAround(coord, tilesList):
    black = 0
    neighbors = getneighborsCoordinates(coord)
    for neighbore in neighbors:
        if neighbore in tilesList:
            if tilesList[neighbore] == BLACK:
                black += 1
    return(black)

def extendtileListToNeighbors(tilesList):
    neighbors = set()
    for coord in tilesList.keys():
        neighbors.update(getneighborsCoordinates(coord))

    for neighbore in neighbors:
        if neighbore not in tilesList:
            tilesList[neighbore] = WHITE

def applyrules(tilesList):
    extendtileListToNeighbors(tilesList)
    newtilesList = tilesList.copy()
    for coord, color in tilesList.items():
        nbBlack = getNumberOfBlacktileAround(coord, tilesList)
        if color == BLACK:
            if nbBlack == 0 or nbBlack > 2:
                newtilesList[coord] = WHITE
        else:
            if nbBlack == 2:
                newtilesList[coord] = BLACK
    return(newtilesList)

if __name__ == '__main__':
    start_time = datetime.now()
    initialtile = (0,0)
    tilesList = {}
    tilesList[initialtile] = WHITE
    nb = 1
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day24.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        matches = re.finditer("(?P<direction>e|se|sw|w|nw|ne)", line)
        currenttile = initialtile
        for matchNum, matchval in enumerate(matches, start=1):
            direction = matchval.group("direction")
            nextPosition = move(currenttile, direction)
            #print(f"*** moving from position {currentPosition} to {nextPosition} ({direction})")
            currenttile = nextPosition
        #print(f"#{nb} - flipping tile {currenttile}")
        if currenttile in tilesList:
            tilesList[currenttile] *= -1
        else:
            tilesList[currenttile] = BLACK
        nb += 1
    f.close()

    print(f"*** Star 1 (Day 0): {countBlack(tilesList)}")


    for i in range(100):
        tilesList = applyrules(tilesList)
        print(f"Day {i+1}: {countBlack(tilesList)}")



    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
