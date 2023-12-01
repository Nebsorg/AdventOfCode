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

f = open("Z:/donnees/developpement/Python/AdventOfCode/2019_Day1.txt", "r")
fuelNeededForModule = 0
totalFuelNeeded = 0
for line in f:
    mass = int(line.rstrip("\n"))
    fuel = int(mass/3)-2
    fuelNeededForModule += fuel
    ## calulate additional fuel
    fuelForFuel = int(fuel/3)-2
    additionalFuelNeeded = 0
    while fuelForFuel > 0:
        additionalFuelNeeded += fuelForFuel
        fuelForFuel = int(fuelForFuel/3)-2
    totalFuelNeeded += fuel + additionalFuelNeeded
    print(f"ModuleMass={mass} - Fuel={fuel} - FuelForFuel={additionalFuelNeeded} - totalModule={fuel+additionalFuelNeeded} - fuelNeededForModule={fuelNeededForModule} - totalFuelNeeded={totalFuelNeeded}")
f.close()

print(f"Star1 : {fuelNeededForModule}")
print(f"Star2 : {totalFuelNeeded}")
