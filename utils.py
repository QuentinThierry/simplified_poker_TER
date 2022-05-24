from random import randrange

from pyparsing import col

# clamp to a min and a max
def clamp(num, min_value, max_value):
    
    if num <= min_value:
        return min_value
    elif num > max_value:
        return max_value
    else:
        return num

# change probability of the given table, always keep sum to 1
def change_proba_of_table(table, row, column, recompense, actionAliceIndice):
    
    alpha = 0.0001
    if(len(table[0]) == 2): #bob
        proba = table[row][actionAliceIndice]
    else:
        proba = table[row] #alice

    ancienneProbaCol = proba[column]
    
    proba[column] = (ancienneProbaCol * (1-alpha)) + (alpha * recompense)
    
    delta = (proba[column] - ancienneProbaCol)
    
    length = len(proba)
    
    if proba[column] < 0:
        delta -= proba[column]
    
    proba[column] = clamp(proba[column], 0, 1)

    exception = 0
    for i in range(length):
        if (i != column) and (proba[i] == 0 and delta > 0) or (proba[i] == 1 and delta < 0):
            exception+=1
    if exception == 3:
        exception = 2
    if exception == 0:
        exception = 1
    
    rest = 0
    
    for i in range(length):
        if i != column:
            proba[i] -= (delta / (length-exception))
            if proba[i] < 0:
                rest += proba[i]
    
    x = -1
    for i in range(length):
        if i != column:
            if proba[i] < 0:
                proba[i] -= rest
                x = i
                break;
        proba[i] = clamp(proba[i], 0, 1)
    
    for i in range(length):
        if (i not in (column, x) and x != -1):
            proba[i] += rest
    
    for i in range(length):
        if proba[i]>=1:
            for y in range(length):
                if i != y:
                    proba[y] = 0
    
    sumProba = sum(proba)
    
    # precision error checker
    if(sumProba >= 1.00000000001 or sumProba <= 0.99999999999):
        rnd = randrange(0,length)
        proba[rnd] += 0.00000000001

