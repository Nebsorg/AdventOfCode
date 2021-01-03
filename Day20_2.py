from datetime import datetime
import math

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3

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
    edges.append(img[0].copy()) ## top
    edges.append(img[len(img)-1].copy()) ## bottom
    colFirst = []
    colLast = []
    for i, line in enumerate(img):
        colFirst.append(line[0])
        colLast.append(line[len(line)-1])
    edges.append(colFirst) ## Left
    edges.append(colLast) ## Right
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
            matches = 0
            edgesDest = getEdges(img)
            for posTile, edgeSource in enumerate(edgesSource):
                for posMatching, edgeDest in enumerate(edgesDest):
                    matching = compareEdges(edgeSource, edgeDest)
                    if matching > 0:
                        result.append((id, posTile, posMatching, matching))
                        break
    return(result)


if __name__ == '__main__':
    start_time = datetime.now()
    tileList = {}
    currentImg = []
    tileId = -1
    readingTile = False
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day20_test.txt", "r")
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
    print(matchList)

    print(f"Star1: {star1}")

    ### constucting full image
    gridSize = int(math.sqrt(len(tileList)))
    fullImage = []
    for i in range(gridSize):
        line = []
        for j in range(gridSize):
            line.append(-1)
        fullImage.append(line)


    print(gridSize)
    print(fullImage)





    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
