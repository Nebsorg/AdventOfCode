from datetime import datetime
import copy


def displayPocketDimension(pocketDimension):
    nbx = set()
    nby = set()
    nbz = set()

    for coord in pocketDimension:
        nbx.add(coord[0])
        nby.add(coord[1])
        nbz.add(coord[2])

    nbx = list(nbx)
    nbx.sort()
    nby = list(nby)
    nby.sort()
    nbz = list(nbz)
    nbz.sort()


    result = ""
    for z in nbz:
        result += f"Z={z}\n"
        result += '  '
        for y in nbx:
            if y >= 0:
                result += str(y)
            else:
                result +=' '
        result+="\n"

        for x in nbx:
            if x >= 0:
                result += str(x) + ' '
            else:
                result += '  '
            for y in nby:
                result += pocketDimension[(x,y,z)]
            result += "\n"
        result += "\n"
    return(result)

def computeNeigboorCoordinate(pos):
    coordinates = []
    computeNeigboorCoordinatePerDimension(list(pos), 0, coordinates)
    ## remove current position
    coordinates.remove(pos)
    return(coordinates)

def computeNeigboorCoordinatePerDimension(pos, dimension, coordinates):
    vecteurs = [-1, 0, 1]

    if dimension == len(pos)-1:
        for shift in vecteurs:
            toTest = pos.copy()
            toTest[dimension] += shift
            coordinates.append(tuple(toTest))
    else:
        for shift in vecteurs:
            toTest = pos.copy()
            toTest[dimension] += shift
            computeNeigboorCoordinatePerDimension(toTest, dimension+1, coordinates)


def getActiveCubeAround(pos, pocketDimension):
    active = 0
    toTests = computeNeigboorCoordinate(pos)
    for coord in toTests:
        if coord in pocketDimension:
            if pocketDimension[coord] == "#":
                active += 1
    return(active)

def updatePocketDimension(pocketDimension, update):
    for coord in update:
        pocketDimension[coord] = update[coord]

def extendPocketDimension(pocketDimension):
    extensions = set()

    actualCoord = list(pocketDimension.keys())
    for coord in actualCoord:
        extensions.update(computeNeigboorCoordinate(coord))

    for coord in extensions:
        if coord in pocketDimension:
            continue
        pocketDimension[coord] = "."

def star(pocketDimension):
    for i in range(6):

        #print(f"Before Round {i+1} - nbActive = {sum(value == '#' for value in pocketDimension.values())}")
        #print(displayPocketDimension(pocketDimension))
        ## extend current pocketDimension to their neighboor :
        extendPocketDimension(pocketDimension)

        cubeToUpdate = {}
        ## checking current status of cube:
        actualCoord = list(pocketDimension.keys())
        ## todo : rajouter les dimension avant et apres ...
        for coord in actualCoord:
            nbActive = getActiveCubeAround(coord, pocketDimension)
            if pocketDimension[coord] == "#":
                if nbActive not in [2,3]:
                    cubeToUpdate[coord] = "."
                    #print(f"{coord} become Inactive")
            else:
                if nbActive == 3:
                    cubeToUpdate[coord] = "#"
        ## updating pocketDimension with the cube to updatedDimension
        updatePocketDimension(pocketDimension, cubeToUpdate)

    nbActive = sum(value == "#" for value in pocketDimension.values())
    return(nbActive)

if __name__ == '__main__':
    start_time = datetime.now()

    pocketDimensionStar1 = {}
    pocketDimensionStar2 = {}
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day17.txt", "r")
    lineId = 0
    for line in f:
         line = list(line.rstrip("\n"))
         for colId in range(len(line)):
             pocketDimensionStar1[(lineId, colId, 0)] = line[colId]
             pocketDimensionStar2[(lineId, colId, 0, 0)] = line[colId]
         lineId += 1
    f.close()

    nbActive = star(pocketDimensionStar1)
    print(f"Star 1 : {nbActive}")
    nbActive = star(pocketDimensionStar2)
    print(f"Star 2 : {nbActive}")

    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
