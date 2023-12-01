from datetime import datetime

print("Day 3 !")

def getSubInstruction(instructions, digitPosition,match):
    subList = []
    for instruction in instructions:
        if instruction[digitPosition] == match:
            subList.append(instruction)
    return(subList)

def evaluate(instructions, digitPosition):
    mask = 0
    for instruction in instructions:
        if instruction[digitPosition] == '1':
            mask += 1
        else:
            mask -= 1
    return(mask)

def secondStar(instructions):
    numberOfDigit = len(instructions[0])

    ## Oxygen
    Oxygen = ""
    instructionsBag = instructions.copy()
    for i in range(numberOfDigit):
        mask = evaluate(instructionsBag, i)
        if mask > 0:
            most = '1'
        elif mask < 0:
            most = '0'
        else:
            most = '1' ## when equal keep the 1 for Oxygen
        instructionsBag = getSubInstruction(instructionsBag, i, most)
        if len(instructionsBag) == 1:
            Oxygen = instructionsBag[0]
            OxygenBin = int(Oxygen, 2)
            break

    ## CO2
    CO2 = ""
    instructionsBag = instructions.copy()
    for i in range(numberOfDigit):
        mask = evaluate(instructionsBag, i)
        if mask > 0:
            least = '0'
        elif mask < 0:
            least = '1'
        else:
            least = '0'  ## when equal keep the 0 for CO2
        instructionsBag = getSubInstruction(instructionsBag, i, least)

        if len(instructionsBag) == 1:
            CO2 = instructionsBag[0]
            CO2Bin = int(CO2, 2)
            break
    print(f"  ** Second Star : Oxygen={Oxygen} -> {OxygenBin} - CO2={CO2} -> {CO2Bin} ** {OxygenBin * CO2Bin}")

def firstStar(instructions):
    numberOfDigit = len(instructions[0])

    ## each digit of mask will indicate if we have more 1 (positive) or more 0 (negative)
    mask = [0] * numberOfDigit
    for instruction in instructions:
        for i in range(numberOfDigit):
            if instruction[i] == '1':
                mask[i] += 1
            else:
                mask[i] -= 1
    gamma = ""
    epsilon = ""
    for i in range(numberOfDigit):
        if mask[i] > 0:
            gamma+='1'
            epsilon+='0'
        else:
            gamma += '0'
            epsilon += '1'

    intGamma = int(gamma, 2)
    intEpsilon = int(epsilon, 2)
    print(f"  ** First Star : gamma={gamma} -> {intGamma} - epsilon={epsilon} -> {intEpsilon} ** {intGamma * intEpsilon}")

start_time = datetime.now()

f = open(".\Day3.txt", "r")
instructions = []
for line in f:
    instructions.append(line.rstrip())
f.close()

firstStar(instructions)
secondStar(instructions)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))