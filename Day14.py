from datetime import datetime
from collections import defaultdict
import re
from bitstring import BitStream, BitArray

regexp = "mem\[(?P<address>\d+)\] = (?P<value>\d+)"
size = 36

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
                address = match.group('address')
                value = int(match.group('value'))
                bitValue = BitArray(uint=value, length=size)
                 ## applying mask :
                bitarray = list(bitValue.bin)
                for position, overload in mask.items():
                    bitarray[position] = overload
                bitValue.bin = ''.join(bitarray)
                memory[address] = bitValue.uint
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
                    bitValue = BitArray(uint=address, length=size)
                    bitarray = list(bitValue.bin)
                    for position, overload in mask.items():
                        bitarray[position] = overload
                    bitValue.bin = ''.join(map(str, bitarray))
                    currentAddress = bitValue.uint
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
