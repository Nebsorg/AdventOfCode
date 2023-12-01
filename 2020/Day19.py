from datetime import datetime

def ruleResolved(innerRule):
    for rule in innerRule:
        if any(map(str.isdigit, rule.split(' '))):
            return(False)
    return(True)

def allResolved(rules):
    for rule in rules.values():
        if not ruleResolved(rule):
            return(False)
    return(True)


def replaceInOneRule(ruleID, newRules, existingRule):
    #print(f"ruleID={ruleID} - newRule={newRules} - existingRule={existingRule}")
    newRuleList = []
    toRemove = []
    for orRule in existingRule:
        orRuleList = orRule.split(' ')
        if str(ruleID) in orRuleList:
            toRemove.append(orRule)
            pos = orRuleList.index(str(ruleID))
            for replacement in newRules:
                ruleSet = orRuleList.copy()
                ruleSet[pos] = replacement
                newRuleList.append(' '.join(ruleSet))
    ## removing element:
    for rule in toRemove:
        existingRule.remove(rule)
    ## adding new one :
    for rule in newRuleList:
        existingRule.append(rule)
    #print(f"ruleID={ruleID} - newRule={newRules} - existingRule={existingRule}")


def replaceInAllRules(ruleID, newRules, rules):
    for innerID, innerRules in rules.items():
        replaceInOneRule(ruleID, newRules, innerRules)

def totallyReplaced(ruleID, rules):
    for innerRules in rules.values():
        for rule in innerRules:
            if str(ruleID) in rule.split(' '):
                return(False)
    return(True)

def resolvedRules(rules):
    resolved = False
    count = 0
    while not resolved and count < 100:
        resolvedId = set()
        for ruleId, innerRule in rules.items():
            if ruleResolved(innerRule):
                print(f"#{count} - rule {ruleId} resolved - replace all instance")
                ## replacing all mention of this rule by it's resolved value
                replaceInAllRules(ruleId, innerRule, rules)
                resolvedId.add(ruleId)
        print(rules)
        ## est-ce qu'il reste encore des reference à cette rule ?
        for id in resolvedId:
            print(f"#{count} - checking resolved ID to remove from rule : {id}")
            if totallyReplaced(id, rules):
                print(f"#{count} - rule {id} totally removed - deleting it")
                del rules[id]

        resolved = allResolved(rules)
        count += 1
    ## removing white space:
    for ruleId, innerRules in rules.items():
        newInner = []
        for rule in innerRules:
            rule = rule.replace(' ', '')
            newInner.append(rule)
        rules[ruleId] = newInner

def resolvedRulesZero(rules):
    resolved = False
    count = 0
    rulesToResolve = set()
    rulesToResolve.add(0)
    print(rulesToResolve)
    while not ruleResolved(rules[0]) and count < 100:
        ruleToAdd = set()
        ruleToRemove = set()
        for ruleId in rulesToResolve:
            print(f"#{count} - checking rule {ruleId}={rules[ruleId]}")
            if not ruleResolved(rules[ruleId]):
                for innerRule in rules[ruleId]:
                    if not ruleResolved(innerRule):
                        neededID = innerRule.split(' ')
                        print(f"#{count} - rule {ruleId} not resolved - adding needID : {neededID}")
                        for id in neededID:
                            if id.isdigit():
                                ruleToAdd.add(int(id))
            else:
                print(f"#{count} - rule {ruleId} resolved - broadcasting value")
                replaceInAllRules(ruleId, rules[ruleId], rules)
                if totallyReplaced(ruleId, rules):
                    print(f"#{count} - rule {ruleId} totally resolved - removing it")
                    ruleToRemove.add(int(ruleId))
        ## adding rule :
        rulesToResolve.update(ruleToAdd)
        rulesToResolve.difference_update(ruleToRemove)
        print(f"#{count} - rule 0 : {rules[0]}")
        
        count += 1
    ## removing white space:
    for ruleId, innerRules in rules.items():
        newInner = []
        for rule in innerRules:
            rule = rule.replace(' ', '')
            newInner.append(rule)
        rules[ruleId] = newInner

if __name__ == '__main__':
    start_time = datetime.now()
    rules = {}
    valid = 0
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day19.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if ':' in line:
            ruleIndex = line.index(':')
            ruleId = int(line[0:ruleIndex])
            if '"' in line:
                rules[ruleId] = [line[ruleIndex+3:ruleIndex+4]]
            else:
                if '|' in line:
                    orIndex = line.index('|')
                    subrule1 = line[ruleIndex+2:orIndex-1]
                    subRule2 = line[orIndex+2:]
                    rules[ruleId] = [subrule1, subRule2]
                else:
                    ## rule line
                    subrule = line[ruleIndex+2:]
                    rules[ruleId] = [subrule]

        elif line == "":
            print(f"Rules:[{rules}]")
            resolvedRulesZero(rules)
            print(f"Rules:[{rules}]")
        else:
            rule0 = rules[0]
            if line in rule0:
                print(f"data={line}")
                valid += 1
    f.close()

    print(f"star1 = {valid}")

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
