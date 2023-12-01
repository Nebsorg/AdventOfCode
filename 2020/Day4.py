import re

MANDATORY = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
RANGE_VALIDATOR = {"byr":(".*byr:(\d+).*", 1920, 2002), "iyr":(".*iyr:(\d+).*", 2010, 2020), "eyr":(".*eyr:(\d+).*", 2020, 2030), "hgtcm":(".*hgt:(\d+)cm.*", 150, 193), "hgtin":(".*hgt:(\d+)in.*", 59, 76)}
REG_VALIDATOR = {"hcl":".*hcl:#(([0-9]|[a-f]){6}).*", "ecl":".*ecl:(amb|blu|brn|gry|grn|hzl|oth).*", "pid":".*pid:(\d+).*"}

def isValide(password):
    for check in MANDATORY:
        if password.get(check) != "Valide":
            #print("Passpord INVALIDE - missing {0}: {1}".format(check, password))
            return(False)
    #print("Passpord VALIDE {0}".format(password))
    return(True)

f = open("Z:\donnees\developpement\Python\AdventOfCode\day4.txt", "r")
validePassport = 0

currentPassword = {}
for line in f:
    if line == "\n":
        #Changing password - validate current one
        if isValide(currentPassword):
            validePassport += 1
        currentPassword = {}
    else:
        #looking for fields
        for key, value in RANGE_VALIDATOR.items():
            result = re.match(value[0], line)
            if result:
                digit = int(result.group(1))
                if value[1] <= digit <= value[2]:
                    currentPassword[key[0:3]] = "Valide"

        for key, value in REG_VALIDATOR.items():
            result = re.match(value, line)
            if result:
                if key == "pid":
                    if len(result.group(1)) == 9:
                        currentPassword[key] = "Valide"
                else:
                    currentPassword[key] = "Valide"

#validating last password:
if isValide(currentPassword):
    validePassport += 1
f.close()
print("Star 1 : Nombre de valide: %d"%validePassport)

toto = ['a']
print(toto)
el = toto.pop()
print(el)
print(toto)
print(len(toto))
toto = None
print(toto)
print(len(toto))
