from datetime import datetime
from num2words import num2words
import numpy as np

#### Main
print("2024 --- Day 2: Red-Nosed Reports ---")
start_time = datetime.now()

fileToOpen = "./Day02.txt"

def getData(fileToOpen):
    f = open(fileToOpen, "r")
    reports = []
    for line in f:
        report = line.split(" ")
        reports.append([int(x) for x in report])
    return(reports)

def isSafe(report):
    direction = 0
    for i in range(len(report)-1):
        if i == 0:
            if report[i] < report[i+1]:
                direction = 1
            else:
                direction = -1
        
        if direction == 1:
            if (report[i] >= report[i+1]) or (report[i]+3 < report[i+1]):
                return(False)
        else:
            if (report[i] <= report[i+1]) or (report[i]-3 > report[i+1]):
                return(False)
    return(True)

def firstStar(reports):
    safe = []
    for i in range(len(reports)):
        if isSafe(reports[i]):
            safe.append(i)
        
    print(f"****** First Star = {len(safe)}")
    


def secondStar(reports):
    safe = []
    for i in range(len(reports)):
        report = reports[i]
        if isSafe(report):
            safe.append(i)
        else:
            for j in range(len(report)):
                subReport = list(report)
                subReport.pop(j)
                if isSafe(subReport):
                    safe.append(i)
                    break

    print(f"****** Second Star = {len(safe)}")



reports = getData(fileToOpen)
firstStar(reports)
secondStar(reports)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 