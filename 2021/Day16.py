import math
from datetime import datetime
import binascii

from collections import deque



def parsePacket(binaryList):
    # print(f" ** Parsing packet [{binaryList}]")
    version = int(binaryList[:3], 2)
    typeID = int(binaryList[3:6], 2)
    currentPosition = 6
    if typeID == 4:
        ## litteral
        litteralValue = ''
        lastValue = 1
        while lastValue == 1:
            subBinary = binaryList[currentPosition:currentPosition+5]
            litteralValue += subBinary[1:]
            currentPosition += 5
            lastValue = int(subBinary[0])
        #print(f"   litteral parsed : {int(litteralValue, 2)}")
        return(currentPosition, version, int(litteralValue, 2))
    else:
        lengthTypeId = binaryList[currentPosition]
        currentPosition += 1
        numbers = []
        if lengthTypeId == '0':
            ## subPacket lenght provided by the next 15 bits
            subPacketsLenght = int(binaryList[currentPosition:currentPosition+15],2)
            currentPosition += 15
            # print(f"   - Operator type 0 - subpacket size = {subPacketsLenght} bits")
            endPosition = currentPosition + subPacketsLenght
            while currentPosition < endPosition:
                parsedBit, includedVersion, number = parsePacket(binaryList[currentPosition:])
                currentPosition += parsedBit
                version += includedVersion
                numbers.append(number)
        else:
            ## number of subpacket provided by the next 11 bits
            nbOfSubPacket = int(binaryList[currentPosition:currentPosition + 11], 2)
            currentPosition += 11
            # print(f"   - Operator type 1 - Number of SubPacket = {nbOfSubPacket}")
            for i in range(nbOfSubPacket):
                parsedBit, includedVersion, number = parsePacket(binaryList[currentPosition:])
                currentPosition += parsedBit
                version += includedVersion
                numbers.append(number)

    if typeID == 0:
        return (currentPosition, version, sum(numbers))
    elif typeID == 1:
        return (currentPosition, version, math.prod(numbers))
    elif typeID == 2:
        return (currentPosition, version, min(numbers))
    elif typeID == 3:
        return (currentPosition, version, max(numbers))
    elif typeID == 5:
        return (currentPosition, version, 1 if numbers[0] > numbers[1] else 0)
    elif typeID == 6:
        return (currentPosition, version, 1 if numbers[0] < numbers[1] else 0)
    elif typeID == 7:
        return (currentPosition, version, 1 if numbers[0] == numbers[1] else 0)


print("--- Day 16: Packet Decoder ---")
#### Main
start_time = datetime.now()

f = open(".\Day16.txt", "r")
inputHexa = []
for line in f:
    inputHexa.append(line.rstrip())
f.close()

for value in inputHexa:
    binaryList = bin(int(value, 16))
    binaryList = binaryList[2:].zfill(len(value)*4)
    #print(f"*********** Parsing {value} -> [{binaryList}]")
    ## parsing the binary:
    _, version, number = parsePacket(binaryList)
    #print(f" - Parsed ! version = {version} - result = {number}")

print(f"** First Star = {version}")
print(f"** Second Star = {number}")

#print(f"** Second Star = {cost_map[(x_max - 1, y_max - 1)]} - {(end_time - mid_time)}")


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))