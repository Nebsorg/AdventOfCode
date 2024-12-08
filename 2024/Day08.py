from datetime import datetime
from collections import defaultdict

#### Main
print(f"2024 --- Day 8: Resonant Collinearity ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    couverture = defaultdict(lambda: [])

    for i,line in enumerate(f):
        line = line.rstrip()
        for j,frequency in enumerate(line):
            if i == 0:
                max_col = len(line)
            if frequency != '.':
                couverture[frequency].append((i,j))
    else:
        max_row = i+1

    return([(max_row, max_col), couverture])

def createAntinodes_star1(a1, a2):
    delta = (a1[0]-a2[0], a1[1]-a2[1])
    return([(a1[0]+delta[0], a1[1]+delta[1]), (a2[0]-delta[0], a2[1]-delta[1])])

def createAntinodes_star2(a1, a2, boundaries):
    result = set()
    delta = (a1[0]-a2[0], a1[1]-a2[1])
    
    ## getting all antinode from first node in boudaries: 
    new_pos = (a1[0]+delta[0], a1[1]+delta[1])
    while 0 <= new_pos[0] < boundaries[0] and 0 <= new_pos[1] < boundaries[1]:
        result.add(new_pos)
        new_pos = (new_pos[0]+delta[0], new_pos[1]+delta[1])

    ## getting all antinode from second node in boudaries: 
    new_pos = (a2[0]-delta[0], a2[1]-delta[1])
    while 0 <= new_pos[0] < boundaries[0] and 0 <= new_pos[1] < boundaries[1]:
        result.add(new_pos)
        new_pos = (new_pos[0]-delta[0], new_pos[1]-delta[1])
    
    ## adding the two antenna in the list: 
    result.add(a1)
    result.add(a2)
    return(result)

def createAllAntinodes(antennas, boundaries):
    antinodes_star1 = set()
    antinodes_star2 = set()

    for i in range(len(antennas)-1):
        a1 = antennas[i]
        for a2 in antennas[i+1:]:
            result = createAntinodes_star1(a1,a2)
            for an in result:
                if 0 <= an[0] < boundaries[0] and 0 <= an[1] < boundaries[1]:
                    antinodes_star1.add(an)

            result = createAntinodes_star2(a1,a2, boundaries)
            for an in result:
                antinodes_star2.add(an)

    return(antinodes_star1, antinodes_star2)

def stars(instructions):
    star1 = 0
    star2 = 0

    boundaries = instructions[0]
    couverture = instructions[1]
    
    antinodes_star1 = set()
    antinodes_star2 = set()

    for antennas in couverture.values():
        as1, as2 = createAllAntinodes(antennas, boundaries)
        antinodes_star1.update(as1)
        antinodes_star2.update(as2)

    star1 = len(antinodes_star1)
    star2 = len(antinodes_star2)

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day08.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 