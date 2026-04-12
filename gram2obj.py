#reads in grammar.txt and converts it to python object:
#   read file, preprocess, load json, validate?

import json
import re

ATOM = "ATOM"

#terminals are {uppercase + _}
def isNonTerm(s):
    s = s.replace("_","")
    return s.upper() and s.isalpha()

def load(fname):
    with open(fname, r) as file:
        content = file.read()
    pre = re.sub(r"\b([\w$]+)\b",r'"\1"',content)
    pre = re.sub(r'"\s+"',' ',pre) # "city":"New" "York" -> "city":"New York"
    obj = json.loads(pre)
    return obj

    #"Validate" basic idea: every non-term referenced in grammar must exist in grammar
    #   I think even while building grammar I want to enforce this...
    '''
    non_terms = set() #all non-terminals
    for k in obj.keys():
        for i in obj[k]:
            non_terms.add(i['name'])
    for k in obj.keys():
        for ...
    '''
'''
Notes: OK, so I need to be thoughtful about "seq" format, esp when building grammar
    There certainly need to be options, e.g. WITH in create token
    ***Something to capture "whatever is between these two non-terms"
        e.g. TRIGGERED_ABIL seq = [(when, whenever, at), *TRIGGER*, ',', EFFECT]
                *TRIGGER* should capture all tokens until comma

'''