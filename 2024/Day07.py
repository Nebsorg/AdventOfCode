from datetime import datetime

#### Main
print(f"2024 --- Day 7: Bridge Repair ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = []

    for line in f:
        line = line.rstrip()
        total = int(line.split(': ')[0])
        operandes = [int(x) for x in line.split(': ')[1].split(' ')]
        instructions.append([total, operandes])
    return(instructions)


def computeStar1(target, operandes):
    possibilities = [operandes[0]]
    nexts = operandes[1:]

    for currentOperand in nexts:
        tempPos = []
        for currentTotal in possibilities:
            result = currentTotal + currentOperand
            if result <= target:
                tempPos.append(result)
                
            result = currentTotal * currentOperand
            if result <= target:
                tempPos.append(result)
        possibilities = tempPos

    # print(f"{target=} - {len(possibilities)}")

    if target in possibilities:
        return(True)
    else:
        return(False)

def computeStar2(target, operandes):
    possibilities = [operandes[0]]
    nexts = operandes[1:]

    for currentOperand in nexts:
        tempPos = []
        for currentTotal in possibilities:
            result = currentTotal + currentOperand
            if result <= target:
                tempPos.append(result)
                
            result = currentTotal * currentOperand
            if result <= target:
                tempPos.append(result)
            
            result = int(str(currentTotal)+str(currentOperand))
            if result <= target:
                tempPos.append(result)

        possibilities = tempPos

    #print(f"{target=} - {possibilities}")

    if target in possibilities:
        return(True)
    else:
        return(False)

def stars(instructions):
    star1 = 0
    star2 = 0

    for i, instruction in enumerate(instructions):
        total = instruction[0]
        operandes = instruction[1]

        if computeStar1(total, operandes):
            star1 += total
        if computeStar2(total, operandes):
            star2 += total


    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day07.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 