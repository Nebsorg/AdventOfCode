def ChercheDouble(listeNombre):
    for i in range(0, len(listeNombre)-1):
        for j in range(i+1, len(listeNombre)):
            if (listeNombre[i]+listeNombre[j]) == 2020:
                return (listeNombre[i]*listeNombre[j])


def ChercheTriple(listeNombre):
    for i in range(0, len(listeNombre)-2):
        for j in range(i+1, len(listeNombre)-1):
            for k in range(j+1, len(listeNombre)):
                if (listeNombre[i]+listeNombre[j]+listeNombre[k]) == 2020:
                    return(listeNombre[i]*listeNombre[j]*listeNombre[k])

f = open(".\Day1.txt", "r")
listOfInt = []
for line in f:
    listOfInt.append(int(line))
f.close()

listOfInt.sort()

print("Double: %d" % ChercheDouble(listOfInt))
print("Triple: %d" % ChercheTriple(listOfInt))
