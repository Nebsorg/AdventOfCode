from datetime import datetime
import re

#### Main
print(f"2024 --- Day 3: Mull It Over ---")
start_time = datetime.now()

regexp = "(mul\((?P<op1>\d{1,3}),(?P<op2>\d{1,3})\))|(do\(\))|(don\'t\(\))"

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = []
    for line in f:
        line = line.rstrip()
        instructions.append(line)
    return(instructions)

def stars(instructions):
    star1 = 0
    star2 = 0
    do = True

    for instruction in instructions:
        matches = re.finditer(regexp, instruction)
        for match in matches:
            if match.group() == "don't()":
                do = False
            elif match.group() == "do()":
                do = True
            else :
                op1 = int(match.group('op1'))
                op2 = int(match.group('op2'))
                star1 += op1*op2
                if do:
                    star2 += op1*op2
            
    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day03.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 