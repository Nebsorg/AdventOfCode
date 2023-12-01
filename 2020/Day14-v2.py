from datetime import datetime
import re

regexp = "mem\[(?P<address>\d+)\] = (?P<value>\d+)"
size = 36


class BitList():
    def __init__(self, _uint):
        BitList.bitList = [0]*size
        BitList.uint = _uint
        BitList.intToBitList()

    def __str__(self):
        return(''.join(map(str, BitList.bitList)))

    def intToBitList():
        n = BitList.uint
        index = size-1
        while n > 0:
            if n%2 != 0:
                BitList.bitList[index] = 1
            n = int(n / 2)
            index -= 1

    def to_uint(self):
        value = 0
        for i in range(size):
            if BitList.bitList[size-i-1] == 1:
                value += 2**i
        BitList.uint = value
        return(value)

def parseMaskStar1(mask):
    dictMask = {}
    listMask = list(mask)
    for i in range(len(listMask)):
        if listMask[i] != 'X':
            dictMask[i] = listMask[i]
    return(dictMask)


def generateAllMasks(mask, resultat):
    mask_val = list(mask.values())
    mask_key = list(mask.keys())
    if 'X' in mask_val:
        ## get associated key :
        key = mask_key[mask_val.index('X')]

        ## changing X in 1:
        mask1 = mask.copy()
        mask1[key] = 1
        generateAllMasks(mask1, resultat)
        mask0 = mask.copy()
        mask0[key] = 0
        generateAllMasks(mask0, resultat)
        return(resultat)
    else:
        resultat.append(mask)

def parseMaskStar2(mask):
    dictMask = {}
    listMask = list(mask)
    for i in range(len(listMask)):
        if listMask[i] != '0':
            dictMask[i] = listMask[i]
    return(dictMask)

def star1():
    memory = {}
    mask = ""
    size = 36
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day14.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if line[0:4] == "mask":
            mask = parseMaskStar1(line[7:])
        else:
            match = re.match(regexp, line)
            if match:
                address = int(match.group('address'))
                value = int(match.group('value'))
                bl = BitList(value)
                for position, overload in mask.items():
                    bl.bitList[position] = int(overload)
                bl.to_uint()
                memory[address] = bl.uint
            else:
                print(f"Error Parsing line {line}")
    f.close()
    total = 0
    for address, value in memory.items():
        total += value
    print(f"Star1 = {total}")

def star2():
    memory = {}
    mask = ""
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day14.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if line[0:4] == "mask":
            mask = parseMaskStar2(line[7:])
            masks = []
            generateAllMasks(mask, masks)
        else:
            match = re.match(regexp, line)
            if match:
                address = int(match.group('address'))
                value = int(match.group('value'))
                for i in range(len(masks)):
                    mask = masks[i]
                    bl = BitList(address)
                    for position, overload in mask.items():
                        bl.bitList[position] = int(overload)
                    bl.to_uint()
                    currentAddress = bl.uint
                    memory[currentAddress] = value
            else:
                print(f"Error Parsing line {line}")
    f.close()
    total = 0
    for address, value in memory.items():
        total += value
    print(f"Star2 = {total}")

if __name__ == '__main__':
    start_time = datetime.now()


    star1()
    star2()
    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
