import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 7: The Treachery of Whales ---")

def star2BrutForce(instructions):
    ## Brut force
    minFuel = 0
    minValue = 0
    start = min(instructions)
    end = max(instructions)

    for i in range(start,end+1):
        fuelNeeded = 0
        for v in instructions:
            fuelNeeded += abs(i-v)*(abs(i-v)+1)/2

        if (i == 0) or (fuelNeeded < minFuel):
            minFuel = int(fuelNeeded)
            minValue = i
    print(f"  ** Second Star Brute Force: minValue = {minValue} - minFuel = {minFuel}")

def star2(instructions):
    ## zoning aroung average value
    avg = int(statistics.mean(instructions))

    ## initialising with average value
    minValue = instructions[0]
    minFuel = sum([abs(v-minValue)*(abs(v-minValue)+1)/2 for v in instructions])

    for i in [0,1,-1]:
        testValue = abs(avg-i)
        fuelNeeded = sum([abs(v-testValue)*(abs(v-testValue)+1)/2 for v in instructions])

        if fuelNeeded < minFuel:
            minFuel = int(fuelNeeded)
            minValue = testValue
    print(f"  ** Second Star Voisinage: minValue = {minValue} - minFuel = {minFuel}")

start_time = datetime.now()
instructions = []

f = open(".\Day7_test.txt", "r")
for line in f:
    instructions = [int(v) for v in line.rstrip().split(",")]
f.close()

median = statistics.median(instructions)
avg = statistics.mean(instructions)
print(f"avg={avg} - int(avg)={int(avg)} - round(avg)={round(avg)} - floor(avg)={math.floor(avg)}- median={median} - int(median)={int(median)} - round(median)={round(median)}")

median = int(median)
fuelNeeded = int(sum([abs(v-median) for v in instructions]))
print(f"  ** First Star : minValue = {median} - minFuel = {fuelNeeded}")

avg = round(avg)
#fuelNeeded = int(sum([abs(v-avg)*(abs(v-avg)+1)/2 for v in instructions]))
#print(f"  ** Second Star avg: minValue = {avg} - minFuel = {fuelNeeded}")


star2(instructions)
#star2BrutForce(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))