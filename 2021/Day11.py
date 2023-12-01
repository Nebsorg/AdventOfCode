import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 11: Dumbo Octopus ---")

#### Main
start_time = datetime.now()

instructions = []
f = open(".\Day11.txt", "r")
for line in f:
    instructions.append([int(v) for v in list(line.rstrip())])
f.close()
#print(instructions)
shifts = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]

size = len(instructions)
nbOfFlash = 0
allFlashedNumber = -1
i = 0

while allFlashedNumber == -1:
    flashed = set()
    completed = False

    ## First Step : increase all by 1:
    for x in range(size):
        for y in range(size):
            instructions[x][y] += 1

    ## Seconde Step : flash & propagate
    while(not completed):
        completed = True
        for x in range(size):
            for y in range(size):
                if (x,y) not in flashed:
                    if instructions[x][y] > 9:
                        flashed.add((x,y))
                        completed = False
                        ## propagate
                        for shift in shifts:
                            xShift = x+shift[0]
                            yShift = y + shift[1]
                            if 0 <= xShift < size and 0 <= yShift < size:
                                instructions[xShift][yShift] += 1
    ## Third Step : set flashed to 0
    for v in flashed:
        instructions[v[0]][v[1]] = 0

    ## star 1 : stop counting after 100
    if i < 100:
        nbOfFlash += len(flashed)

    #print(f"Step {i} : nbFlashed={len(flashed)} - Total={nbOfFlash} - {instructions} - ")

    ## is all the octopuss flashed simultaneously ? :
    if len(flashed) == size * size:
        #print(f"Step {i} : They all Flashed !")
        allFlashedNumber = i + 1
    i += 1

print(f"  ** First Star : {nbOfFlash}")
print(f"  ** Second Star : {allFlashedNumber}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))