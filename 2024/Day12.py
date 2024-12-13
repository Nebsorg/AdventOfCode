from datetime import datetime
from collections import defaultdict
import copy

#### Main
print(f"2024 --- Day 12: Garden Groups ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    instructions = []
    ## read all instruction : 

    for i,line in enumerate(f):
        line = line.rstrip()
        #instructions.append([[x, False] for x in list(line)])
        instructions.append(list(line))
    return(instructions)

def getVoisinsInGarden(pos, max_row, max_col):
    shifts = [(0,1), (0,-1), (1,0), (-1,0)]
    result = set()

    for shift in shifts:
        new_pos = (pos[0]+shift[0], pos[1]+shift[1])
        if 0 <= new_pos[0] < max_row and 0 <= new_pos[1] < max_col:
            result.add(new_pos)
    return(result)

def getAroundCoordinates(pos):
    shifts = [(0,1), (0,-1), (1,0), (-1,0)]
    result = set()

    for shift in shifts:
        new_pos = (pos[0]+shift[0], pos[1]+shift[1])
        result.add(new_pos)
    return(result)

def scanRegion(id, pos, garden, treated):
    new_regions = set()
    voisins = getVoisinsInGarden(pos, len(garden), len(garden[0]))

    for voisin in voisins:
        if voisin in treated:
            continue
        
        if garden[voisin[0]][voisin[1]] == id:
            new_regions.add(voisin)
            treated.add(voisin)
            new_regions.update(scanRegion(id, voisin, garden, treated))

    return(new_regions)



def createRegions(garden):
    max_row = len(garden)
    max_col = len(garden[0])
    
    treatedPosition = set()
    regionID = 0
    regions = defaultdict(lambda: set())

    for i in range(max_row):
        for j in range(max_col):

            if (i,j) in treatedPosition:
                #print(f"{i,j}={garden[i][j]} - already treated - skipped")
                continue
            
            regionName = garden[i][j]
            regions[regionID].add((i,j))
            new_treated = set()
            regions[regionID].update(scanRegion(regionName, (i,j), garden, new_treated))
            treatedPosition.update(new_treated)
            #print(f"{i,j}={regionName} - treated - {regionID}={regions[regionID]}")
            regionID += 1

    return(regions)

def evalRegionStar1(region_coordinate):
    # nb fence = number of voisin pas dans la region
    # aire : nb d'element

    fences = 0
    for val in region_coordinate:
        voisins = getAroundCoordinates(val)
        for voisin in voisins:
            if not(voisin in region_coordinate):
                fences += 1

    return(fences)

def evalRegionStar2(region_coordinate):
    corners = 0
    for position in region_coordinate:
        ## Create a bool for if each surrounding tile is "in region""
        N = ((position[0], position[1]-1) in region_coordinate)
        E = ((position[0]+1, position[1]) in region_coordinate)
        S = ((position[0], position[1]+1) in region_coordinate)
        W = ((position[0]-1, position[1]) in region_coordinate)
        NE = ((position[0]+1, position[1]-1) in region_coordinate)
        SE = ((position[0]+1, position[1]+1) in region_coordinate)
        NW = ((position[0]-1, position[1]-1) in region_coordinate)
        SW = ((position[0]-1, position[1]+1) in region_coordinate)

        # une position peut etre un coin dans plusieurs configuration 
        # tout seul : +4
        if(not N and not E and not S and not W): corners+=4

        # pointe (un seul adjacent)
        if(N and not E and not S and not W): corners+=2
        if(E and not S and not W and not N): corners+=2
        if(S and not W and not N and not E): corners+=2
        if(W and not N and not E and not S): corners+=2

        # convex
        if(S and E and not N and not W): corners+=1
        if(S and W and not N and not E): corners+=1
        if(N and E and not S and not W): corners+=1
        if(N and W and not S and not E): corners+=1

        # concave
        if(E and N and not NE): corners+=1
        if(E and S and not SE): corners+=1
        if(W and N and not NW): corners+=1
        if(W and S and not SW): corners+=1

    return(corners)


def stars(garden):
    star1 = 0
    star2 = 0

    
    regions = createRegions(garden)
    
    for regionId, region_coord in regions.items():
        area = len(region_coord)

        fences = evalRegionStar1(region_coord)
        star1 += fences*area

        corners = evalRegionStar2(region_coord)
        #print(f"Evaluation of region  {regionId} = {area, corners}")
        star2 += corners*area
       

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day12.txt"

instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 