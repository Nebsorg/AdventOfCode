import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 9: Smoke Basin ---")

def star1(instructions):
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    height = len(instructions)
    width = len(instructions[0])

    risks = []
    lowPoints = []
    for line in range(height):
        for col in range(width):
            adjacentValues = []
            for shift in shifts:
                testLine = line + shift[0]
                testCol = col + shift[1]

                if (testLine >= 0) and (testLine < height) and (testCol >= 0) and (testCol < width):
                    adjacentValues.append(instructions[testLine][testCol])
            if instructions[line][col] < min(adjacentValues):
                risks.append(instructions[line][col]+1)
                lowPoints.append((line, col))
    print(f"  ** First Star : {sum(risks)}")
    return(lowPoints)

def star2(instructions, lowpoints):
    shifts = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    height = len(instructions)
    width = len(instructions[0])

    basinList = {}
    for lowpoint in lowpoints:
        basinList[lowpoint] = set()
        basinList[lowpoint].add(lowpoint)
        nextPointBag = [lowpoint]
        while(len(nextPointBag) > 0):
            currentPoint = nextPointBag.pop()
            for shift in shifts:
                testLine = currentPoint[0] + shift[0]
                testCol = currentPoint[1] + shift[1]
                if (testLine >= 0) and (testLine < height) and (testCol >= 0) and (testCol < width):
                    if instructions[testLine][testCol] > instructions[currentPoint[0]][currentPoint[1]] and instructions[testLine][testCol] != 9:
                        ## this point is part of the basin
                        nextPointBag.append((testLine, testCol))
                        basinList[lowpoint].add((testLine,testCol))

    basinSize = []
    for k,v in basinList.items():
        basinSize.append(len(v))
    basinSize.sort()
    print(f"  ** Second Star : {math.prod(basinSize[-3:])}")

#### Main
start_time = datetime.now()
instructions = []

f = open(".\Day9.txt", "r")
instructions = []
for line in f:
    instructions.append([int(v) for v in list(line.rstrip())])
f.close()

lowPoints = star1(instructions)
star2(instructions, lowPoints)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))