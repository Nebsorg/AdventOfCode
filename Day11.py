from datetime import datetime
import copy

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

def star1(layout):
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
    return(countOccupiedSeat(layout), iteration)

def star2(layout):
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
    return(countOccupiedSeat(layout), iteration)

def getLayout():
    layout = []
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day11.txt", "r")
    for line in f:
         layout.append(list(line.rstrip("\n")))
    f.close()
    return(layout)

if __name__ == '__main__':
    start_time = datetime.now()

    layout = []
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day11.txt", "r")
    for line in f:
         layout.append(list(line.rstrip("\n")))
    f.close()
    result, iteration = star1(layout)
    print(f"star1: {result} ({iteration} iteration)")
    result, iteration = star2(layout)
    print(f"star2: {result} ({iteration} iteration)")

    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
