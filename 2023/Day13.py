from datetime import datetime
import copy
from tools import Style

#### Main
print(f"{Style.RED}2023 --- Day 13: Point of Incidence ---{Style.RESET}")
start_time = datetime.now()

def getLine(pattern, line_id):
    if 0 <= line_id < len(pattern):
        return(pattern[line_id])
    else:
        return([])

def getColumn(pattern, col_id):
    if 0 <= col_id < len(pattern[0]):
        result = []
        for i in range(len(pattern)):
            result.append(pattern[i][col_id])
        return(result)
    else:
        return([])

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    patterns = {}
    pattern_id = 0
    patterns[pattern_id] = []
    for line in f:
        line = line.rstrip()
        if line == '':
            pattern_id += 1
            patterns[pattern_id] = []
            continue
        
        patterns[pattern_id].append(list(line))
    return(patterns)


def getVerticalSymetry(pattern):
    col_max = len(pattern[0])
    symetries = []

    for i in range(0,col_max-1):
        col_to_compare = min(i+1, col_max-i-1)
        for j in range(col_to_compare):
            col1 = getColumn(pattern, i-j)
            col2 = getColumn(pattern, i+j+1)
            if col1 != col2:
                break
        else:
            symetries.append(i)
    return(symetries)

def getHorizontalSymetry(pattern):
    row_max = len(pattern)
    symetries = []
    for i in range(0,row_max-1):
        row_to_compare = min(i+1, row_max-i-1)
        for j in range(row_to_compare):
            row1 = getLine(pattern, i-j)
            row2 = getLine(pattern, i+j+1)
            if row1 != row2:
                break
        else:
            symetries.append(i)
    return(symetries)

def smudgePattern(pattern, row, col):
    new_pattern = copy.deepcopy(pattern)
    if new_pattern[row][col] == '.':
        new_pattern[row][col] = '#'
    else:
        new_pattern[row][col] = '.'
    return(new_pattern)

def findSmudgeSymetry(id, pattern):
    old_vertical_symetry = getVerticalSymetry(pattern)
    old_horizontal_symetry = getHorizontalSymetry(pattern)
    for row in range(len(pattern)):
        for col in range(len(pattern[0])):
            corrected_pattern = smudgePattern(pattern, row, col)

            result = getVerticalSymetry(corrected_pattern)
            new_result = [d for d in result if d not in old_vertical_symetry]
            if len(new_result) > 0 :
                return(new_result[0]+1)

            result = getHorizontalSymetry(corrected_pattern)
            new_result = [d for d in result if d not in old_horizontal_symetry]
            if len(new_result)>0:
                return((new_result[0]+1)*100)
                
    print(f"{id} : No new symetry found - return old one")
    return(0)

def stars(patterns):
    star1 = 0
    star2 = 0
    for pattern in patterns.values():
        vertical_symetry = getVerticalSymetry(pattern)
        if len(vertical_symetry) > 0:
            star1 += vertical_symetry[0]+1

        horizontal_symetry = getHorizontalSymetry(pattern)
        if len(horizontal_symetry) > 0:
            star1 += (horizontal_symetry[0]+1)*100

        star2 += findSmudgeSymetry(id, pattern)

    print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")  
    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day13.txt"
patterns = readInstruction(fileToOpen)

stars(patterns)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 