f = open("Z:\donnees\developpement\Python\AdventOfCode\day6.txt", "r")
currentGroupStar1 = set()
currentGroupStar2 = set()
totalSumStar1 = 0
totalSumStar2 = 0
nbMemberGroup = 0
for line in f:
    if line == "\n":
        ## Star 1 : counting element of current group(contain only unique question which have been answered yes)
        totalSumStar1 += len(currentGroupStar1)
        currentGroupStar1 = set()

        ## Star2 :
        totalSumStar2 += len(currentGroupStar2)
        currentGroupStar2 = set()
        nbMemberGroup = 0
    else:
        answers = list(line.rstrip("\n"))

        ## Star 1:
        currentGroupStar1.update(answers)

        ## Star 2:
        nbMemberGroup += 1
        if nbMemberGroup == 1:
            currentGroupStar2.update(answers)
        else:
            ## on ne garde que l'intersection des reponses et de la liste existantes
            currentGroupStar2 = currentGroupStar2.intersection(answers)

## don't forget final group :
totalSumStar1 += len(currentGroupStar1)
totalSumStar2 += len(currentGroupStar2)
f.close()

print("Star 1 : {0}".format(totalSumStar1))
print("Star 2 : {0}".format(totalSumStar2))
