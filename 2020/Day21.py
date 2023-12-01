from datetime import datetime
import copy
from collections import defaultdict

if __name__ == '__main__':
    start_time = datetime.now()
    menuList = []
    foodlist = defaultdict(lambda: set())
    alergenlist = defaultdict(lambda: set())
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day21.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        #print(line)
        line = line.split(' ')
        ingredients = []
        alergens = []
        section = "ingredients"
        for str in line:
            if '(' in str:
                section = "alergen"
            else:
                if section == "ingredients":
                    ingredients.append(str)
                else:
                    alergens.append(str.replace(')', '').replace(',', ''))
        #print(f"ingredient : {ingredients}")
        #print(f"alergens : {alergens}")
        menuList.append([ingredients, alergens])
        for ingredient in ingredients:
            foodlist[ingredient].update(alergens)

        for alergen in alergens:
            alergenlist[alergen].update(ingredients)

    f.close()
    print(f"menu : {menuList}")
    print(f"FoodList with potential Alergen : {foodlist}")
    print(f"Alergen in potential food : {alergenlist}")

    ## For each alergen, reducing the list to ingredients appearing each time:
    filteredAlergen = {}
    for alergen in alergenlist:
        commonIngredients = set()
        for line in menuList:
            if alergen in line[1]:
                if len(commonIngredients) == 0:
                    commonIngredients = set(line[0])
                else:
                    commonIngredients = commonIngredients.intersection(line[0])
        filteredAlergen[alergen] = commonIngredients
    print(f"filtered alergen in potential food : {filteredAlergen}")

    ## removing solved alergen (ie with only one ingredient)
    finished = False
    while not finished:
        finished = True
        for alergen, ingredients in filteredAlergen.items():
            if len(ingredients) == 1:
                ingredientToRemove = max(ingredients)
                ## remove the ingredient from the other alergen:
                for subalergen, subingredients in filteredAlergen.items():
                    if subalergen != alergen:
                        if ingredientToRemove in subingredients:
                            subingredients.remove(ingredientToRemove)
                            finished = False
    print(f"filtered alergen in potential food (reduced): {filteredAlergen}")

    ## identfiying safe ingredient:
    ingredientsReduced = {}
    safeIngredient = {}
    for ingredient in foodlist:
        ingredientsReduced[ingredient] = []
        for alergen, ingredients in filteredAlergen.items():
            if ingredient in ingredients:
                ingredientsReduced[ingredient].append(alergen)
                break
        if len(ingredientsReduced[ingredient]) == 0:
            safeIngredient[ingredient] = 0
    print(f"filtered ingredient : {ingredientsReduced}")
    print(f"safe ingredient : {safeIngredient}")

    ## couting number of time they appeargind :
    star1 = 0
    for ingredient in safeIngredient:
        for line in menuList:
            if ingredient in line[0]:
                safeIngredient[ingredient] += 1
                star1 += 1
    print(f"safe ingredient : {safeIngredient}")
    print(f"star1 = {star1}")

    ## creating star2 answer
    sortedAlergen = list(filteredAlergen.keys())
    sortedAlergen.sort()
    print(sortedAlergen)
    star2 = ""
    for i, alergen in enumerate(sortedAlergen):
        if i == len(sortedAlergen)-1:
            star2 += max(filteredAlergen[alergen])
        else:
            star2 += max(filteredAlergen[alergen]) + ","
    print(f"star2 = {star2}")


    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
