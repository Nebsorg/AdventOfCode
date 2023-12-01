from datetime import datetime
import re
import regex

def ruleResolved(innerRule):
    if len(getRuleIdinRule(innerRule)) > 0:
        return(False)
    return(True)

def allResolved(rules):
    for rule in rules.values():
        if not ruleResolved(rule):
            return(False)
    return(True)

def replaceInAllRules(ruleID, newRules, rules):
    for innerID, innerRules in rules.items():
        rules[innerID] = innerRules.replace(f"({ruleID})", f"({newRules})")

def getRuleIdinRule(rule):
    id = set()
    matches = re.finditer("(?P<ID>(\d+))", rule)
    for matchNum, matchval in enumerate(matches, start=1):
        id.add(int(matchval.group("ID")))
    return(list(id))

def resolvedRulesZero(rules):
    resolved = False
    count = 0
    rulesToResolve = set()
    rulesToResolve.add(0)
    while not ruleResolved(rules[0]) > 0 and count < 100:
        ruleToAdd = set()
        ruleToRemove = set()
        for ruleId in rulesToResolve:
            unresolvedIDs = getRuleIdinRule(rules[ruleId])
            if len(unresolvedIDs) > 0:
                ruleToAdd.update(unresolvedIDs)
            else:
                replaceInAllRules(ruleId, rules[ruleId], rules)
                ruleToRemove.add(ruleId)
        ## adding rule :
        rulesToResolve.update(ruleToAdd)
        rulesToResolve.difference_update(ruleToRemove)
        count += 1
        print(f"#{count} - Size of RuleToresolve: {len(rulesToResolve)}")

if __name__ == '__main__':
    start_time = datetime.now()

    rules = {}
    lineMatchingStar1 = []
    lineMatchingStar2 = []
    lineToAnalyse = []
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day19.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if ':' in line:
            ruleIndex = line.index(':')
            ruleId = int(line[0:ruleIndex])
            if '"' in line:
                rules[ruleId] = line[ruleIndex+3:ruleIndex+4]
            else:
                ## put number in brackets
                numbers = re.compile(r'(\d+)')
                rules[ruleId] = numbers.sub(r'(\1)', line[ruleIndex+2:]).replace(' ', '')
        elif line == "":
            rulesStar1 = rules.copy()
            ruleStar2  = rules.copy()
        else:
            lineToAnalyse.append(line)
    f.close()

    ## star1 :
    resolvedRulesZero(rulesStar1)
    rule0 = rulesStar1[0]
    for line in lineToAnalyse:
        match = re.match(rule0, line)
        if match:
            if len(line) == len(match.group(0)):
                lineMatchingStar1.append(line)
    print(f"star1 = {len(lineMatchingStar1)}")

    ### star 2 : updating rules
    ruleStar2[8]="42+"
    rules[11] = "(?P<R> 42 (?&R)? 31 )"  # recursive pattern

    print(ruleStar2)
    resolvedRulesZero(ruleStar2)
    rule0 = ruleStar2[0]
    print(rule0)
    for line in lineToAnalyse:
        r = regex.compile(rule0)
        match = r.fullmatch(line)
        if match:
            lineMatchingStar2.append(line)
    print(f"star2 = {len(lineMatchingStar2)}")



    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
