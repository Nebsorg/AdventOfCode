import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 12: Passage Pathing ---")

#### Main
start_time = datetime.now()

def howManyTimeInRoad(cave, currentRoad):
    count = 0
    for v in currentRoad:
        if cave == v:
            count += 1
    return(count)

def exploreStar1(connections, currentRoad, possibleRoad):
    currentPosition = currentRoad[-1]

    if currentPosition == 'end':
        return(currentRoad)
    else:
        for nextPos in connections[currentPosition]:
            if nextPos == 'start':
                continue

            if nextPos.islower():
                count = howManyTimeInRoad(nextPos, currentRoad)
                if count > 0:
                    continue

            followingRoad = currentRoad.copy()
            followingRoad.append(nextPos)
            result = exploreStar1(connections, followingRoad, possibleRoad)
            if result != None:
                possibleRoad.append(result)

def exploreStar2(connections, currentRoad, possibleRoad, smallCaveVisitedTwice):
    currentPosition = currentRoad[-1]

    if currentPosition == 'end':
        #print(f"This path is completed ! : {currentRoad} - {possibleRoad}")
        return(currentRoad)
    else:
        for nextPos in connections[currentPosition]:
            alreadyVisited = smallCaveVisitedTwice
            if nextPos == 'start':
                continue

            if nextPos.islower():
                count = howManyTimeInRoad(nextPos, currentRoad)
                if count > 1:
                    continue
                if count == 1:
                    if alreadyVisited == True:
                        continue
                    else:
                        ## keep it, but mark we have visited small cave twice already
                        alreadyVisited = True

            followingRoad = currentRoad.copy()
            followingRoad.append(nextPos)
            result = exploreStar2(connections, followingRoad, possibleRoad, alreadyVisited)
            if result != None:
                possibleRoad.append(result)


connections = defaultdict(lambda: set())
f = open(".\Day12.txt", "r")
for line in f:
    input = line.rstrip().split('-')
    connections[input[0]].add(input[1])
    connections[input[1]].add(input[0])
f.close()

currentRoad = ['start']
possibleRoad = []
result = exploreStar1(connections, currentRoad, possibleRoad)
print(f"** First Star : {len(possibleRoad)}")


currentRoad = ['start']
possibleRoad = []
smallCaveVisitedTwice = False
result = exploreStar2(connections, currentRoad, possibleRoad, smallCaveVisitedTwice)
print(f"** Second Star : {len(possibleRoad)}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))