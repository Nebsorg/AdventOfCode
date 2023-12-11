from datetime import datetime
import copy
import math

#### Main
print("2023 --- Day 11: Cosmic Expansion ---")
start_time = datetime.now()

def readInstruction(file):
    galaxy_id = 1
    f = open(file, "r")
    ## read all instruction : 
    sky = []
    galaxies = {}
    for i, line in enumerate(f):
        newline = []
        line = line.rstrip()
        for j,val in enumerate(line):
            if val == '#':
                galaxies[galaxy_id] = [i,j]
                galaxy_id += 1
            newline.append(val)
        sky.append(newline)        
    return(sky, galaxies)


def expend_galaxy(sky, galaxies, expension_size):
    row_with_expension = []
    col_with_expension = []
    
    expended_galaxies = copy.deepcopy(galaxies)
    ## identify empty row
    for i in range(len(sky)):
        row = sky[i]
        if row.count('.') == len(row):
            ## empty row
            row_with_expension.append(i)

    ## identify empty column
    for j in range(len(sky[0])):
        col = [sky[d][j] for d in range(len(sky))]
        if col.count('.') == len(col):
            col_with_expension.append(j)

    ## expending Galaxy : 
    for galaxy_pos in expended_galaxies.values():
        row_count = sum(i < galaxy_pos[0] for i in row_with_expension)
        col_count = sum(i < galaxy_pos[1] for i in col_with_expension)
        galaxy_pos[0] += row_count * (expension_size-1)
        galaxy_pos[1] += col_count * (expension_size-1)

    return(expended_galaxies)

def distances(galaxies):
    result = 0
    galaxy_list = list(galaxies.keys())
    for i, g1 in enumerate(galaxy_list):
        for g2 in galaxy_list[i+1:len(galaxy_list)]:
            result += abs(galaxies[g1][0]-galaxies[g2][0]) + abs(galaxies[g1][1]-galaxies[g2][1])
    return(result)

def stars(sky, galaxies):
    expended_galaxies_star1 = expend_galaxy(sky, galaxies, 2)
    expended_galaxies_star2 = expend_galaxy(sky, galaxies, 1000000)

    print(f"****** First Star = {distances(expended_galaxies_star1)}")
    print(f"****** Second Star = {distances(expended_galaxies_star2)}")



fileToOpen = "./2023/Day11.txt"
sky, galaxies = readInstruction(fileToOpen)


stars(sky, galaxies)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 