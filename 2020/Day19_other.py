#!/usr/bin/env python
import sys
import regex

# Kudos to https://github.com/taddeus/advent-of-code/blob/master/2020/19_regex.py
def solve(rules, messages):
    def expand(value):
        if not value.isdigit(): return value
        return "(?:" + "".join(map(expand, rules[value].split())) + ")"

    r = regex.compile(expand("0"))
    return sum(r.fullmatch(m) is not None for m in messages)


f = open("Z:\donnees\developpement\Python\AdventOfCode\day19.txt", "r")
raw_rules, messages = f.read().split("\n\n")
messages = messages.splitlines()
rules = dict(
    raw_rule.replace('"', "").split(": ", 1)
    for raw_rule in raw_rules.splitlines()
)

print(solve(rules, messages))
rules["8"] = "42 +"  # repeat pattern
rules["11"] = "(?P<R> 42 (?&R)? 31 )"  # recursive pattern
print(solve(rules, messages))
