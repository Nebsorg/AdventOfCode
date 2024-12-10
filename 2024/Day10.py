from datetime import datetime
import copy

#### Main
print(f"2024 --- Day 10: Hoof It ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    #instructions = []
    ## read all instruction : 
    starts = []
    area = []

    for i,line in enumerate(f):
        line = line.rstrip()
        area.append([int(x) for x in line])
        for j, val in enumerate(line):
            if val == '0':
                starts.append((i,j))
    
    return([starts, area])

def getneighbors(pos, area):
    shifts = [(0,1), (0,-1), (-1,0), (1,0)]
    neighbors = []
    max_row = len(area)
    max_col = len(area[0])

    for shift in shifts:
        new_pos = (pos[0]+shift[0], pos[1]+shift[1])
        if 0 <= new_pos[0] < max_row and 0 <= new_pos[1] < max_col:
            if area[new_pos[0]][new_pos[1]] == area[pos[0]][pos[1]] + 1 :
                neighbors.append(new_pos)
    return(neighbors)

def getTrail_star1(pos, area):
    if area[pos[0]][pos[1]] == 9:
        ## this 9 has been reached from this start, must not be counted again
        area[pos[0]][pos[1]] = -1
        return(1)
    
    trails = 0
    neighbors = getneighbors(pos, area)

    for nb in neighbors:
        trails += getTrail_star1(nb, area)

    return(trails)

def getTrail_star2(pos, area):
    if area[pos[0]][pos[1]] == 9:
        return(1)
    
    trails = 0
    neighbors = getneighbors(pos, area)

    for nb in neighbors:
        trails += getTrail_star2(nb, area)

    return(trails)


def stars(instructions):
    star1 = 0
    star2 = 0

    starts = instructions[0]
    area = instructions[1]

    for start in starts:
        test_area = copy.deepcopy(area)
        star2 += getTrail_star2(start, test_area)
        star1 += getTrail_star1(start, test_area)

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day10.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 