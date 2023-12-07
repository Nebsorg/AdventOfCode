

## renvoie l'interval intersection des deux intervales [min,max] ou [] si pas d'intersection
def interval_intersection(i1,i2):
    xmin = min(i1[0],i1[1])
    xmax = max(i1[0],i1[1])
    ymin = min(i2[0],i2[1])
    ymax = max(i2[0],i2[1])

    if (ymin > xmax) or (xmin > ymax):
        return([])
    
    imin = max(xmin, ymin)
    imax = min(xmax, ymax)
    return([imin, imax])

## renvoie le decouvage en nouveaux interval avec borne commune
def interval_spread_included(i1,i2):
    result = []
    intersection = interval_intersection(i1,i2)
    if len(intersection) == 0:
        result.append(i1)
        result.append(i2)
        return(result)

    values = []
    values.extend(i1)
    values.extend(i2)
    values.extend(intersection)

    ## return the new intervals : 
    values = sorted(values)
    for i in range(0, len(values), 2):
        result.append([values[i], values[i+1]])
    return(result)

## renvoie le decouvage en nouveaux interval avec borne exclus en dehors de l'intersection
def interval_spread_excluded(i1,i2):
    result = []
    intersection = interval_intersection(i1,i2)
    if len(intersection) == 0:
        result.append(i1)
        result.append(i2)
        return(result)

    values = []
    val_min = min(min(i1), min(i2))
    val_max = max(max(i1), max(i2))

    if intersection[0] > val_min:
        values.extend([val_min, intersection[0]-1, intersection[0]])
    else: 
        values.append(intersection[0])

    if intersection[1] < val_max:
        values.extend([val_max, intersection[1]+1, intersection[1]])
    else: 
        values.append(intersection[1])

    values = sorted(values)
    for i in range(0, len(values), 2):
        result.append([values[i], values[i+1]])
    return(result)
                  
# si l'intervale 2 divise l'interval 1, renvoie les nouveaux intervals composé de l'interval 1
# si pas d'intersection, renvoi l'interval 1
def split_interval_with_interval(i1,i2):
    result = []
    intersection = interval_intersection(i1,i2)
    if len(intersection) == 0:
        result.append(i1)
        return(result)
    
    values = []
    val_min = min(i1)
    val_max = max(i1)

    if intersection[0] > val_min:
        values.extend([val_min, intersection[0]-1, intersection[0]])
    else: 
        values.append(intersection[0])

    if intersection[1] < val_max:
        values.extend([val_max, intersection[1]+1, intersection[1]])
    else: 
        values.append(intersection[1])

    values = sorted(values)
    for i in range(0, len(values), 2):
        result.append([values[i], values[i+1]])
    return(result)

# on supprime l'interval 2 de l'interval 1, et on renvoit les intervalles obtenus.
# si pas d'intersection, renvoi l'interval inchangé
def extract_interval_from_interval(i1,i2):
    intersection = interval_intersection(i1,i2)
    result  = split_interval_with_interval(i1,i2)
    result.remove(intersection)
    return(result)
