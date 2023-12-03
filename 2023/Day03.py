from datetime import datetime
import re
import math

#### Main
print("2023 --- Day 3: Gear Ratios ---")
start_time = datetime.now()

fileToOpen = "./2023/Day03.txt"

regExp_number = "(\d+)"
regExp_symbole = "[^.\d]+"

f = open(fileToOpen, "r")

symboles = []
numbers = []
for i, line in enumerate(f):
    line = line.rstrip()
    
    ## get numbers (value, (line, column range))
    matches = re.finditer(regExp_number, line)
    for match in matches:
        numbers.append((int(match.group()), (i, match.span())))
    
    ## get symboles (value, (line, column))
    matches = re.finditer(regExp_symbole, line)
    for match in matches:
        symboles.append((match.group(), (i, match.start())))

## determine numbers around symboles : 
sum_part = 0
sum_gear = 0
for symbole in symboles:
    syb_val = symbole[0]
    syb_row = symbole[1][0]
    syb_col = symbole[1][1]

    voisinage = []

    for number in numbers:
        num_val = number[0]
        num_row = number[1][0]
        num_range = range(number[1][1][0], number[1][1][1])

        if (syb_row-1) <= num_row <= (syb_row+1):
            if ((syb_col-1) in num_range) or ((syb_col) in num_range) or ((syb_col+1) in num_range):
                #print(f"{num_val} (pos={num_row}/{num_range}) au voisinage de {syb_val} (pos={syb_row}/{syb_col})")
                sum_part+=num_val
                voisinage.append(num_val)

    ## testing gear: 
    if (syb_val == '*') and (len(voisinage)>=2):
        gear_ratio = math.prod(voisinage)
        print(f"gear trouvé en (pos={syb_row}/{syb_col}) - voisinnage = {voisinage} - puissance={gear_ratio}")
        sum_gear += gear_ratio

print(f"****** First Star = {sum_part}")
print(f"****** Second Star = {sum_gear}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 