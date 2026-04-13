import atomize
import gram2obj
from pprint import pprint
import re

'''
GRAMMAR = {
    "EFFECT": [
        {
            "name": "CREATE_TOKEN",
            "pattern": ["create", "N", "PT", "COLOR", "CTYPE", "creature", "token"],
            "slots": ["N", "PT", "COLOR", "CTYPE"],
            "output": {
                "type": "CREATE",
                "num": "$N",
                "pt": "$PT",
                "color": "$COLOR",
                "ctype": "$CTYPE"
            }
        },
        {
            "name": "DRAW",
            "pattern": ["draw", "N", "cards"],
            "slots": ["N"],
            "output": {
                "type": "DRAW",
                "count": "$N"
            }
        }
    ]
}
'''

#for old funcs, see git

#non-terminals in grammar are {uppercase + _}
def isNonTerm(s):
    s = s.replace("_","")
    return s.isupper() and s.isalpha()

def match_pattern(tokens, rule, start=0):
    pattern = rule["seq"]

    i = start #needed?
    j = 0
    
    FALSE_VAL = -1

    in_star = False
    while i < len(tokens) and j < len(pattern):
        curr = tokens[i]
        #DON'T OVERUSE THIS!
        #Leave periods and commas in <tokens> for readability, but match with
        #   "PERIOD" and "COMMA" in grammar for ease of use
        if curr == ".": curr = "PERIOD"
        elif curr == ",": curr = "COMMA"
        
        expected = pattern[j]
        
        if not in_star and expected == "*":
            in_star = True
            j += 1
                
        optional = False
        if expected[-1] == "?":
            optional = True
            expected = expected[:-1]
            
        found = False
        for e in expected.split("|"):
            temp = curr
            if not(isNonTerm(e)): temp = temp.lower()
            if e == temp:
                i += 1
                j += 1
                found = True
                in_star = False
                break
        if not found:
            if in_star:
                i += 1
            elif optional:
                j += 1
            else:
                #print("\t*Mandatory token not matched:",rule['name'],":",i,j)
                return FALSE_VAL

    if j == len(pattern):
        return i #token index of where pattern ended!
    else:
        #print("\t*Pattern not finished:",rule['name'],":",i,j)
        return FALSE_VAL

def parse_with_grammar(grammar, text):
    text,subs = atomize.atomize(text)
    #just append to subs!
    #   for now, "replaced"s generated here will be list of toks instead of single string, but that's OK?
    tokens = atomize.smart_split(text)
    print("BEFORE", tokens)

    for i in range(len(grammar)):
        rule = grammar[i]
        for start in range(len(tokens)):
            end = match_pattern(tokens, rule,start)
            if end != -1:
                n = rule['name']
                subs.append((n,tokens[start:end])) #BEFORE changing tokens
                tokens = tokens[:start] + [n] + tokens[end:]
                i = 0 #RESTART rules!
                break

    return tokens, subs
    #how to detect "failure"? I guess leftover literals...

if __name__ == '__main__':
    grammar = gram2obj.load("grammar.txt")
    tests = [
        "Create a 1/1 green Saproling creature token.",
        "Create a 4/4 white Angel creature token with flying.",
        "Draw two cards.",
        "At the beginning of your upkeep, draw two cards.",
        "Destroy target creature."
    ]
    
    for t in tests:
        print(t)
        tokens, subs = parse_with_grammar(grammar,t)
        print("AFTER ", tokens)
        pprint(subs)
        print()
    
