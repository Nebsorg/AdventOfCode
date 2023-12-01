import re
from collections import defaultdict

FirstLevelRegExp = "(?P<outerBox>.*) bags contain (?P<inside>(\d [a-zA-Z ]* bags?(, |.))+|no other bags.)"
SecondLevelRegExp = "(?P<Nb>\d) (?P<name>[a-zA-Z ]*) bags?"
myBag = "shiny gold"


def star1():
    possibleHolder = set()
    searchedBag = []
    searchedBag.append(myBag)
    while len(searchedBag) > 0:
        bag = searchedBag.pop()
        if bag in BagContainIn:
            possibleHolder.update(BagContainIn[bag])
            searchedBag.extend(BagContainIn[bag])
    print("Star1 : Nb holder = {0}".format(len(possibleHolder)))

def star2(currentBag):
    totalBags = 0
    if currentBag in BagContenersRules:
        innerBags = BagContenersRules[currentBag]
        if len(innerBags) > 0:
            for inBagName, inBagNb in innerBags.items():
                totalBags += inBagNb + inBagNb * star2(inBagName)
            return(totalBags)
        else:
            return(0)

f = open("Z:\donnees\developpement\Python\AdventOfCode\day7.txt", "r")
validePassport = 0

BagContenersRules = {}
BagContainIn = defaultdict(lambda: [])
for line in f:
    line = line.rstrip("\n")

    match = re.match(FirstLevelRegExp, line)

    if match:
        outerBoxName = match.group('outerBox')
        insideStr = match.group('inside')

        insideList = {}
        matches = re.finditer(SecondLevelRegExp, insideStr)
        for matchNum, matchval in enumerate(matches, start=1):
            boxName = matchval.group("name")
            nbBox = matchval.group("Nb")
            insideList[boxName] = int(nbBox)
            BagContainIn[boxName].append(outerBoxName)

        BagContenersRules[outerBoxName] = insideList
    else:
        print("Error in parsing of line {0}".format(line))
f.close()

star1()
bagStar2 = star2(myBag)
print("Star2 : {0}".format(bagStar2))
