import math
from datetime import datetime
import re

regExp = "target area: x=(?P<xmin>-?\d*)..(?P<xmax>-?\d*), y=(?P<ymin>-?\d*)..(?P<ymax>-?\d*)"
print("--- Day 17: Trick Shot ---")

def fire(velocity, target):
    probe_position =  [0,0]
    current_velocity = [velocity[0], velocity[1]]

    maxYReached = 0
    bottomY = min(target[0][1], target[1][1])
    while probe_position[1] > bottomY:
        ## updating probe position
        probe_position[0] += current_velocity[0]
        probe_position[1] += current_velocity[1]

        ## updating velocity
        if current_velocity[0] > 0:
            current_velocity[0] -= 1
        elif current_velocity[0] < 0 :
            current_velocity[0] += 1
        current_velocity[1] -= 1

        ## updating max y reached
        if probe_position[1] > maxYReached:
            maxYReached = probe_position[1]

        ## test if on target and returning max Y if true
        if target[0][0] <= probe_position[0] <= target[1][0] and target[0][1] <= probe_position[1] <= target[1][1]:
            return(maxYReached)

    ## target missed ! (prove is deeper than the target)
    return(-1)

#### Main
start_time = datetime.now()

f = open(".\Day17.txt", "r")
for line in f:
    match = re.match(regExp, line)
    if match:
        target = ((int(match.group('xmin')), int(match.group('ymin'))), (int(match.group('xmax')), int(match.group('ymax'))))
f.close()

xRange = max(target[0][0], target[1][0])
yRange = min(target[0][1], target[1][1])
bestVelocity = None
yReachedMax = 0
successShot = set()
for vx in range(abs(xRange)+1):
    for vy in range(abs(yRange)+1):
        for direction in [-1,1]:
            yReached = fire((vx,vy*direction), target)
            if yReached >= 0:
                successShot.add((vx, vy*direction))
                if bestVelocity == None:
                    bestVelocity = (vx, vy*direction)
                else:
                    if yReached > yReachedMax:
                        yReachedMax = yReached
                        bestVelocity = (vx, vy * direction)

print(f"** First Star : {yReachedMax} (reached with velocity {bestVelocity})")
print(f"** Second Star : {len(successShot)}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))