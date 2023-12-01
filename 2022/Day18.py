from datetime import datetime
import math
import copy
from collections import defaultdict


def getSides(cube_coordinates):
    sides = []
    for i in [-1,1]:
        sides.append((cube_coordinates[0]+i, cube_coordinates[1], cube_coordinates[2]))
        sides.append((cube_coordinates[0], cube_coordinates[1]+i, cube_coordinates[2]))
        sides.append((cube_coordinates[0], cube_coordinates[1], cube_coordinates[2]+i))
    return(sides)

def getUncoveredSide(cubes):
    all_coordinates = [x for x in cubes.values()]
    uncovered_sides = []
    for cube in cubes.values(): 
        sides = getSides(cube)
        for side in sides: 
            if side in all_coordinates:
                continue
            else:
                uncovered_sides.append(side)
    return(uncovered_sides)

def secondStar(cubes, uncovered_sides):
    
    ## identifying connected uncovered_sides
    unique_uncovered_sides = set(uncovered_sides)
    print(f"uncovered size = {len(uncovered_sides)} - unique uncovered size = {len(unique_uncovered_sides)}")
    
    ## verifying all uncovered sides: 
    edges_side = []
    trapped_side = []

    unique_uncovered_sides = set(uncovered_sides)
    
    connectedSidesBags = defaultdict(lambda:set())
    currentSide = 1
    max = len(unique_uncovered_sides)
    while len(unique_uncovered_sides) > 0:
        side = unique_uncovered_sides.pop()
        print(f"** {currentSide} / {max} : Treating uncovered side {side}")
        nearSides = getSides(side)

        for nearSide in nearSides:
            ## is this side an uncovered_side ? 
            if nearSide in uncovered_sides:
                ## yes, checking if this near side is in a bag to add current side in same bag:
                for bagId, sides in connectedSidesBags.items():
                    if nearSide in sides:
                        currentBag = bagId
                        print(f"   - uncovered side {side} : neighboorg {nearSide} found in bag {bagId} -- adding it in same bag : {currentBag}")
                        break
                else:
                    ## no bag found, creating a new one
                    currentBag = len(connectedSidesBags)
                    print(f"   - uncovered side {side} : neighboorg {nearSide} not found in bag -- creating a new one : {currentBag}")
                connectedSidesBags[currentBag].add(side)
                break
        else:
            print(f"   - uncovered side {side} do not have any nnearboorg in uncoveredside !!")
        currentSide += 1

                

            
    print(connectedSidesBags)

    star = 0

    return(star)


def secondStar_bis(cubes, uncovered_sides):
    ## verifying all uncovered sides: 
    edges_side = []
    trapped_side = []

    unique_uncovered_sides = set(uncovered_sides)
    print(f"uncovered size = {len(uncovered_sides)} - unique uncovered size = {len(unique_uncovered_sides)}")
    
    for side in unique_uncovered_sides:
        ## testing if this side is in the middle or on the edges:
        ## if at least one cube is found in every direction : the cube is trapped inside
        ## getting max and min cube in every direction : 
        ##is there higher or lower block on same (x,y) ? --> it must be max or min to be on edge
        z_layer = [x[2] for x in cubes.values() if (x[0] == side[0] and x[1] == side[1])]
        z_layer = set(z_layer)
        ##is there higher or lower block on same (x,z) ? --> it must be max or min to be on edge
        y_layer = [x[1] for x in cubes.values() if (x[0] == side[0] and x[2] == side[2])]
        y_layer = set(y_layer)
        ##is there higher or lower block on same (y,z) ? --> it must be max or min to be on edge
        x_layer = [x[0] for x in cubes.values() if (x[1] == side[1] and x[2] == side[2])]
        x_layer = set(x_layer)
        
        if len(z_layer) >= 2 and len(x_layer) >= 2 and len(y_layer) >= 2: 
            ## they are several block for each layer
            ## testing relative position : if each coordinate are between min/max for each direction --> trapped
            if (min(x_layer) < side[0] < max(x_layer)) and ((min(y_layer) < side[1] < max(y_layer))) and (min(z_layer) < side[2] < max(z_layer)):
                trapped_side.append(side)
                print(f"testing side {side} - x_layer={x_layer} - y_layer={y_layer} - z_layer={z_layer} --> inside")
            else: 
                edges_side.append(side)
                #print(f"testing side {side} - x_layer={x_layer} - y_layer={y_layer} - z_layer={z_layer} --> on the edge")
        else:
            edges_side.append(side)
            #print(f"testing side {side} - x_layer={x_layer} - y_layer={y_layer} - z_layer={z_layer} --> on the edge")

    star = 0
    for side in uncovered_sides:
        if side in trapped_side:
            continue
        star += 1

    return(star)

#### Main
print("2022 --- Day 18: Boiling Boulders ---")
start_time = datetime.now()


network = {}
f = open(".\Day18_test.txt", "r")
cubes = {}
for i, line in enumerate(f):
    line = line.rstrip()
    cubes[i] = tuple([int(x) for x in line.split(',')])

uncovered_sides = getUncoveredSide(cubes)
print(f"****** First Star = {len(uncovered_sides)}")
star = secondStar(cubes, uncovered_sides)
star = 0
print(f"****** Second Star = {star}")                

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 