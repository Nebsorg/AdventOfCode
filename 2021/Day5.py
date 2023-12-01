from datetime import datetime
from collections import defaultdict
import re

start_time = datetime.now()
print("Day 5 !")
regExp = "(?P<x1>\d*),(?P<y1>\d*) -> (?P<x2>\d*),(?P<y2>\d*)"

f = open(".\Day5.txt", "r")
impactedPointStar1 = defaultdict(lambda: 0)
impactedPointStar2 = defaultdict(lambda: 0)
for line in f:
    line = line.rstrip("\n")
    match = re.match(regExp, line)
    if match:
        ## Star 1 : keeping only horizontal & vertical line
        x1 = int(match.group('x1'))
        y1 = int(match.group('y1'))
        x2 = int(match.group('x2'))
        y2 = int(match.group('y2'))

        if (x1 == x2):
            # vertical line
            for i in range(min(y1,y2), max(y1,y2)+1):
                impactedPointStar1[(x1, i)] += 1
                impactedPointStar2[(x1, i)] += 1
        elif (y1 == y2):
            # horizontal line
            for i in range(min(x1,x2), max(x1,x2) + 1):
                impactedPointStar1[(i, y1)] += 1
                impactedPointStar2[(i, y1)] += 1
        else:
            ## sorting vector from min x to max x:
            if x1 > x2:
                xStart = x2
                yStart = y2
                xEnd = x1
                yEnd = y1
            else:
                xStart = x1
                yStart = y1
                xEnd = x2
                yEnd = y2

            coefDir = int((yEnd-yStart) / (xEnd-xStart))
            for i in range(xEnd - xStart + 1):
                impactedPointStar2[(xStart + i, yStart + i * coefDir)] += 1
    else:
        print("Error in parsing of line {0}".format(line))
f.close()

## dangerous point :
dangerousStar1 = sum([1 for v in impactedPointStar1.values() if v > 1])
dangerousStar2 = sum([1 for v in impactedPointStar2.values() if v > 1])
print(f"  ** First Star : Number of dangerous points = {dangerousStar1}")
print(f"  ** Second Star : Number of dangerous points = {dangerousStar2}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))