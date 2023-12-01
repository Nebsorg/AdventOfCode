from datetime import datetime

def star1(bus):
    bus = [int(x) for x in bus if x != 'x']
    nextPassage = [targetTime + (x - targetTime%x) for x in bus]
    minIndex = nextPassage.index(min(nextPassage))
    print(f"Star 1 = {(nextPassage[minIndex]-targetTime)*bus[minIndex]} - bus[{minIndex}]={bus[minIndex]} - min={nextPassage[minIndex]}")

def star2(bus):
    shiftBus = {}
    for i in range(len(bus)):
        if bus[i] != 'x':
            id = int(bus[i])
            shiftBus[id] = i

    currentTime = 1
    increment = 1
    iteration = 1
    for id, shift in shiftBus.items():
        while (currentTime + shift)%id != 0:
            ## on cherche le premier diviseur pour cette id
            iteration += 1
            currentTime += increment
        increment *= id ## avant de passer au bus suivant, on s'assure que le prochain horaire sera toujours un multiple de précedant (bus + shift)
    print(f"Star 2 = {currentTime} (en {iteration} iterations)")

if __name__ == '__main__':
    start_time = datetime.now()

    lineNb = 0
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day13.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if lineNb == 0:
            targetTime = int(line)
        elif lineNb == 1:
            bus = line.split(',')
        lineNb += 1
    f.close()

    star1(bus)
    star2(bus)

    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
