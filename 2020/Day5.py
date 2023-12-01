
def decode(instructions, posmax):
    min = 0
    max=posmax
    indexMax = len(instructions)-1
    for i in range(indexMax):
        mid = (((max+1) - min) / 2) + min
        if instructions[i] in ['F', 'L']:
            max = mid - 1
        else:
            min = mid

    if instructions[indexMax] in ['F', 'L']:
        return(int(min))
    else:
        return(int(max))

def getMySeat(occupiedSeats):
    previousUnoccupiedId = -1
    for i in range(128):
        for j in range(8):
            id = i*8+j
            if id in occupiedSeats:
                continue

            if (id-1) != previousUnoccupiedId:
                return(id)
            previousUnoccupiedId = id

f = open("Z:\donnees\developpement\Python\AdventOfCode\day5.txt", "r")
occupiedSeats = []
highestID = 0
for line in f:
    boarding = list(line.rstrip("\n"))
    row = decode(boarding[:7], 127)
    col = decode(boarding[7:], 7)
    id = 8*row+col

    if id > highestID:
        highestID = id
    occupiedSeats.append(id)
f.close()

print("HighestId = {0}".format(highestID))
print("Nomber of seats Occupied = {0}".format(len(occupiedSeats)))
print("My seat ID = {0}".format(getMySeat(occupiedSeats)))
