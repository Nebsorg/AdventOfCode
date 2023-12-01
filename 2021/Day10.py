import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 10: Syntax Scoring ---")

#### Main
start_time = datetime.now()

instructions = []
f = open(".\Day10.txt", "r")
for line in f:
    instructions.append(list(line.rstrip()))
f.close()

chunks = {}
chunks[')'] = ('(', 3, 1)
chunks[']'] = ('[', 57, 2)
chunks['}'] = ('{', 1197, 3)
chunks['>'] = ('<', 25137, 4)
openChunk = dict((v[0], k) for k, v in chunks.items())
closeChunk = chunks.keys()

scoreStar1 = 0
scoresStar2 = []

for i, line in enumerate(instructions):
    stack = []

    for v in list(line):
        if v in closeChunk:
            if len(stack) == 0 or chunks[v][0] != stack[-1]:
                ## invalide line
                scoreStar1 += chunks[v][1]
                break
            else:
                stack.pop()
        else:
            stack.append(v)
    else:
        ## incomplete line
        score = 0
        while(len(stack)>0):
            open = stack.pop()
            close = openChunk[open]
            score = score * 5 + chunks[close][2]
        scoresStar2.append(score)

scoresStar2.sort()
print(f"  ** First Star : {scoreStar1}")
print(f"  ** Second Star : {scoresStar2[int((len(scoresStar2)-1)/2)]}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))