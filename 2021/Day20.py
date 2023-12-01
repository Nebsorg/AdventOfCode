import copy
import math
from datetime import datetime
import re
from ast import literal_eval

print("--- Day 20: Trench Map ---")
reg_list = "\[(?P<left>\d*),(?P<right>\d*)\]"
#### Main
start_time = datetime.now()


def displayPicture(picture):
    for line in picture:
        print(''.join(line))

def enhancePicture(inputImage, enhancementAlgo, extendValue):
    ## start by increase picture size by x element around
    extendBy = 2
    xMax = len(inputImage[0])

    extendedImage = []

    for i in range(5):
        extendedImage.append([extendValue]*(xMax+2*extendBy))
    for line in inputImage:

        extendedImage.append(([extendValue]*extendBy) + line + ([extendValue]*extendBy))
    for i in range(5):
        extendedImage.append([extendValue]*(xMax+2*extendBy))

    ## Enhence extended Image :
    outputImage = []
    shifts = [-1, 0, 1]

    yMax = len(extendedImage)
    xMax = len(extendedImage[0])

    ## constructing output image per pixel
    for y in range(yMax):
        currentLine = []
        for x in range(xMax):
            index = ''
            for yshift in shifts:
                inputY = y + yshift
                for xshift in shifts:
                    inputX = x + xshift
                    if 0 <= inputX < xMax and 0 <= inputY < yMax:
                        index += extendedImage[inputY][inputX]
                    else:
                        index += extendValue

            ## checking value in algo:
            indexInt = int(index, 2)
            # print(f"  - created index is {index} - {indexInt}  --> {enhancementAlgo[indexInt]}")

            currentLine.append(enhancementAlgo[indexInt])
        outputImage.append(currentLine)
    return (outputImage)

def bothStars(inputImage, enhancementAlgo):
    extendValue = '0'
    result = copy.deepcopy(inputImage)
    for i in range(50):
        result = enhancePicture(result, enhancementAlgo, extendValue)
        if i == 1:
            brightPoints = sum([v.count('1') for v in result])
            print(f"** First Star : {brightPoints}")
        extendValue = enhancementAlgo[int(extendValue * 9, 2)]

    brightPoints = sum([v.count('1') for v in result])
    print(f"** Second Star : {brightPoints}")

f = open(".\Day20.txt", "r")
lineID = 0
inputImage = []
for line in f:
    if lineID == 0:
        enhancementAlgo = line.rstrip().replace('#', '1').replace('.', '0')
    elif lineID >=2:
        inputImage.append(list(line.rstrip().replace('#', '1').replace('.', '0')))
    lineID += 1
f.close()

bothStars(inputImage, enhancementAlgo)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))