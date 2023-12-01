import re

print("Day2")

f = open(".\day2.txt", "r")
validePasswordStar1 = 0
validePasswordStar2 = 0
for line in f:
    result = re.match("(\d+)-(\d+) (\w): (.+)", line)
    if result:
        min = int(result.group(1))
        max = int(result.group(2))
        char = result.group(3)
        mdp = result.group(4)

        # Star 1
        occurence = mdp.count(char)
        if (occurence >= min) and (occurence <= max):
            validePasswordStar1 += 1

        #Star 2
        if ((mdp[min-1] == char) and (mdp[max-1] != char)) or \
            ((mdp[max-1] == char) and (mdp[min-1] != char)):
            validePasswordStar2 +=1
f.close()
print("Star 1 : Nombre de valide: %d"%validePasswordStar1)
print("Star 2 : Nombre de valide: %d"%validePasswordStar2)
