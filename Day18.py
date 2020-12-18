from datetime import datetime
import copy


def extractFirstLevel(expression):
    nbOpen = 0
    poslist = []
    for pos,c in enumerate(expression):
        if c == '(':
            nbOpen += 1
            if nbOpen == 1:
                posOpen = pos
        elif c == ')':
            nbOpen -= 1
            if nbOpen == 0:
                poslist.append((posOpen, pos))
    return(poslist)

def evaluateExpressionStar1(expression):
    if '(' in expression:
        ## identify first level of parenthesis
        subExps = extractFirstLevel(expression)
        newExpression = []
        pos = 0
        while pos < len(expression):
            for subExp in subExps:
                if pos == subExp[0]:
                    ## il faut remplacer la valeur
                    value = evaluateExpressionStar1(expression[subExp[0]+1:subExp[1]])
                    newExpression.append(value)
                    pos = subExp[1]+1
                    subExps.remove(subExp)
                    break
            else:
                newExpression.append(expression[pos])
                pos += 1
        return(evaluateExpressionStar1(newExpression))
    else:
        ##evaluating left to right:
        while(len(expression)>1):
            operand1 = int(expression[0])
            operand2 = int(expression[2])
            operator = expression[1]
            if operator == '+': result = operand1 + operand2
            else:  result = operand1 * operand2
            expression = [result] + expression[3:]
        return(expression[0])

def evaluateExpressionStar2(expression):
    if '(' in expression:
        ## identify first level of parenthesis
        subExps = extractFirstLevel(expression)
        newExpression = []
        pos = 0
        while pos < len(expression):
            for subExp in subExps:
                if pos == subExp[0]:
                    value = evaluateExpressionStar2(expression[subExp[0]+1:subExp[1]])
                    newExpression.append(value)
                    pos = subExp[1]+1
                    subExps.remove(subExp)
                    break
            else:
                newExpression.append(expression[pos])
                pos += 1
        return(evaluateExpressionStar2(newExpression))
    else:
        ## evaluating with priority to +
        while '+' in expression:
            index = expression.index('+')
            expression = expression[:index-1] + [int(expression[index-1]) + int(expression[index+1])] + expression[index+2:]

         ## evaluating *:
        while '*' in expression:
            index = expression.index('*')
            expression = expression[:index-1] + [int(expression[index-1]) * int(expression[index+1])] + expression[index+2:]

        return(expression[0])

if __name__ == '__main__':
    start_time = datetime.now()
    star1 = 0
    star2 = 0
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day18.txt", "r")
    for line in f:
        line = list(line.rstrip("\n").replace(' ', ''))
        valueStar1 = evaluateExpressionStar1(line)
        valueStar2 = evaluateExpressionStar2(line)
        star1 += valueStar1
        star2 += valueStar2
    f.close()

    print(f"star1={star1}")
    print(f"star2={star2}")

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
