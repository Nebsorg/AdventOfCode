from datetime import datetime

print("Day 2 !")

def firstStar(instructions):
    depth = 0
    position = 0
    for instruction in instructions:
        if instruction[0] == 'up':
            depth -= int(instruction[1])
        elif instruction[0] == 'down':
            depth += int(instruction[1])
        else: #forward
            position += int(instruction[1])

    print(f"  ** First Star : position={position} - depth={depth} ** {position * depth}")

def secondStar(instructions):
    depth = 0
    position = 0
    aim = 0
    for instruction in instructions:
        if instruction[0] == 'up':
            aim -= int(instruction[1])
        elif instruction[0] == 'down':
            aim += int(instruction[1])
        else:  # forward
            position += int(instruction[1])
            depth += aim*int(instruction[1])

    print(f"  ** Second Star : position={position} - depth={depth} ** {position * depth}")

start_time = datetime.now()

f = open(".\Day2.txt", "r")
instructions = []
for line in f:
    instructions.append(line.split())
f.close()

firstStar(instructions)
secondStar(instructions)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))