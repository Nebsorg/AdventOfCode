import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 8: Seven Segment Search ---")

def star1(instructions):
    unique = 0
    for line in instructions:
        unique += sum([1 for v in line[1] if len(v) in [2,4,3,7]])
    print(f"  ** First Star : {unique}")


def star2(instructions):

    standardMapping = {}
    standardMapping[0] = 'abcefg'
    standardMapping[1] = 'cf'
    standardMapping[2] = 'acdeg'
    standardMapping[3] = 'acdfg'
    standardMapping[4] = 'bcdf'
    standardMapping[5] = 'abdfg'
    standardMapping[6] = 'abdefg'
    standardMapping[7] = 'acf'
    standardMapping[8] = 'abcdefg'
    standardMapping[9] = 'abcdfg'

    sumCode = 0
    for line in instructions:
        decodedMapping = mapSegments(line[0])

        ## remap:
        correctedMapping = {}
        for k,v in standardMapping.items():
            newWord = ""
            for char in v:
                newWord += decodedMapping[char]
            correctedMapping[k] = set(newWord)

        code = ""
        for digit in line[1]:
            for k,v in correctedMapping.items():
                if v == set(digit):
                    code += str(k)
                    # print(f"{digit} --> {k}")
        sumCode += int(code)
        #print(f" ** decoding line {','.join(line[0])} | {','.join(line[1])} --> {code}")
    print(f"  ** Second Star : {sumCode}")



def mapSegments(input):

    ## initialise mapping
    mapping = {}
    for v in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
        mapping[v] = set()

    ## Start with evident number:
    for v in input:
        if len(v) == 3:
            seven = v
        elif len(v) == 2:
            one = v
        elif len(v) == 4:
            four = v
        elif len(v) == 7:
            eight = v

    ## a is the letter in seven not in one :
    mapping['a'].update([v for v in seven if v not in one])

    ## b and d are the letter in 4 but not in 1
    mapping['b'].update([v for v in four if v not in one])
    mapping['d'].update([v for v in four if v not in one])

    ## e and g are the letter in 8 but not in 1, 4 and 7
    mapping['e'] = set(eight) - set(one) - set(four) - set(seven)
    mapping['g'] = set(eight) - set(one) - set(four) - set(seven)

    ## number 2, 3 and 5 are the only one with a lenght of 5 digits
    ## b is the one which appear only one time in 2, 3 and 5, and also in 4:
    nbOccurence = defaultdict(lambda: 0)
    for value in [v for v in input if len(v) == 5]:
        for char in list(value):
            nbOccurence[char] += 1
    mapping['b'] = mapping['b'].intersection([k for k,v in nbOccurence.items() if v == 1])

    ## now d is given by removing b possibility:
    mapping['d'].difference_update(mapping['b'])

    ## now we can indentify 5 : it's the only 5 segments which have b & d and common with 4.
    for value in input:
        if len(value) == 5:
            if list(mapping['b'])[0] in value and list(mapping['d'])[0] in value:
                five = value

    ## now we can identify f : it's the intersection between 4 and 5, minus b, minus d (which are now known)
    intersect = set(five).intersection(set(four))
    #print(intersect)
    intersect.difference_update(mapping['b'])
    intersect.difference_update(mapping['d'])
    mapping['f'] = intersect

    ## now we have f with one : it's what remaing of one when C removed :
    mapping['c'] = set(one)
    mapping['c'].difference_update(mapping['f'])

    ## now we have g with five : it's what remain when your remove a,b,d,f:
    mapping['g'] = set(five)
    mapping['g'].difference_update(set.union(mapping['a'], mapping['b'], mapping['d'], mapping['f']))

    ##finally we have e : it current minus g:
    mapping['e'].difference_update(mapping['g'])

    ## convert set in lit:
    for k,v in mapping.items():
        mapping[k] = list(v)[0]
    return(mapping)

start_time = datetime.now()
instructions = []

f = open(".\Day8.txt", "r")
instructions = []
for line in f:
    signal = line.rstrip().split(" | ")
    input = signal[0].split()
    output = signal[1].split()
    instructions.append([input, output])
f.close()

star1(instructions)
star2(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))