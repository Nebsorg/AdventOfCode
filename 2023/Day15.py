from datetime import datetime
import re
from tools import Style
from collections import defaultdict

#### Main
print(f"{Style.RED}2023 --- Day 15: Lens Library ---{Style.RESET}")
start_time = datetime.now()

regexp = "(?P<box>\w*)(?P<operand>=|-)(?P<lens>\d*)"

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    for line in f:
        line = line.rstrip()
        return(line.split(','))

def evaluate(instruction):
    value = 0
    for c in list(instruction):
        ascii_code = ord(c)
        value += ascii_code
        value *= 17
        value = value%256
    return(value)


def stars(instructions):
    star1 = 0
    star2 = 0

    boxes = defaultdict(lambda: [])
    lenses = {}
    for instruction in instructions:
        star1 += evaluate(instruction)
        matches = re.finditer(regexp, instruction)
        for match in matches:
            label = match.group('box')
            box_id = int(evaluate(label))
            operand = match.group('operand')
            if operand == '=':
                lens = int(match.group('lens'))
            else:
                lens = 0

        content = boxes[box_id]
        if operand == "-":
            if label in content:
                content.remove(label)
                del lenses[label]
        else:
            lenses[label] = (lens, box_id)
            if not (label in content):
                content.append(label)

    ## evaluate focusing power: 
    star2 = 0
    for label, data in lenses.items():
        box_id = data[1]
        focal_lenght = data[0]
        slot = boxes[box_id].index(label)+1

        star2 += (box_id+1) * slot * focal_lenght

    print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")
    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day15.txt"
instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 