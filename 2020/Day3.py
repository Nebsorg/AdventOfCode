slope = []
f = open(".\day3.txt", "r")
for line in f:
    slope.append(list(line.rstrip("\n")))
f.close()

def calculateCollision(shiftX, shiftY, slope):
    currentPositionX = 0
    currentPositionY = 0
    finishLine = len(slope)
    slopeWidth = len(slope[0])
    collision = 0

    while(currentPositionX < finishLine):
        if slope[currentPositionX][currentPositionY] == '#':
            collision += 1
        currentPositionX += shiftX
        currentPositionY = (currentPositionY + shiftY) % slopeWidth
    return(collision)

print("Star 1 : nb of collision = ", calculateCollision(1, 3, slope))
print("Star 2 : nb of collision = ", calculateCollision(1, 1, slope) * calculateCollision(1, 3, slope) * calculateCollision(1, 5, slope) * calculateCollision(1, 7, slope) * calculateCollision(2, 1, slope))
