
import re
import copy

regExp = "(?P<inst>nop|acc|jmp) (?P<value>(\+|-)\d*)"

def testProgram(program, swapInstuction = -1):
    instructionposition = 0
    accumulator = 0
    infiniteLoop = False
    while (instructionposition < len(program)) and not infiniteLoop:
        if program[instructionposition][2] > 0:
            infiniteLoop = True
        else:
            program[instructionposition][2] += 1
            instruction = program[instructionposition][0]
            if instructionposition == swapInstuction:
                if instruction == "jmp":
                    instruction = "nop"
                elif instruction == "nop":
                    instruction = "jmp"
            if instruction == "acc":
                accumulator += program[instructionposition][1]
                instructionposition += 1
            elif instruction == "jmp":
                instructionposition += program[instructionposition][1]
            elif instruction == "nop":
                instructionposition += 1
            else:
                instructionposition += 1
    return infiniteLoop, accumulator

instructions = {}
instructionposition = 0
f = open("Z:\donnees\developpement\Python\AdventOfCode\day8.txt", "r")
for line in f:
    line = line.rstrip("\n")
    match = re.match(regExp, line)

    if match:
        instruction = match.group('inst')
        value = int(match.group('value'))
        instructions[instructionposition] = [instruction, value, 0]
        instructionposition += 1
    else:
        print("Error in parsing of line {0}".format(line))
f.close()

## star1
instructionsStar1 = copy.deepcopy(instructions)
infiniteLoop, accumulator = testProgram(instructionsStar1)
if not infiniteLoop:
    print("Star 1 : Program terminated normaly - accumulator = {0}".format(accumulator))
else:
    print("Star 1 : Program interrupted due to infinite loop - accumulator = {0}".format(accumulator))

## star 2
## creating swaping list:
swappingList = []
for instructionPosition in instructions.keys():
    if instructions[instructionPosition][0] == "jmp" or instructions[instructionPosition][0] == "nop":
        swappingList.append(instructionPosition)

for id in swappingList:
    instructionTest = copy.deepcopy(instructions)
    infiniteLoop, accumulator = testProgram(instructionTest, id)
    if not infiniteLoop:
        print("Star 2 : SwapID {1} - Program terminated normaly - accumulator = {0}".format(accumulator, id))
        break
