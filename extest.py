from pprint import pprint
from process import ctypes
import re

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

NUM_LITS = [
    "a", "an", "one","two","three","four","five","six","seven","eight","nine","ten",
    "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
    "eighteen", "nineteen", "twenty", "ninety-nine"
]

CTYPES = [s.lower() for s in ctypes]

def normalize_tokens(text):
    words = text.lower().split()

    result = []
    for w in words:
        if w in {"white", "blue", "black", "red", "green"}:
            result.append(("COLOR", w))
            continue
        if "/" in w:  # crude PT detection
            result.append(("PT", w))
            continue
        if w in NUM_LITS or re.match(r'^\d+$',w):
            result.append(("N", w))
            continue
        is_ctype = False
        for s in CTYPES:
            if w == s or w == s+"s":
                is_ctype = True
                break
        if is_ctype:
            result.append(("CTYPE", w))
            continue
        result.append(("LITERAL", w))

    return result

def match_pattern(tokens, rule):
    pattern = rule["pattern"]
    slots = {}

    i = 0
    j = 0

    while i < len(tokens) and j < len(pattern):
        token_type, token_value = tokens[i]
        expected = pattern[j]

        if expected == token_type:
            slots[expected] = token_value
            i += 1
            j += 1
        elif expected == token_value:
            i += 1
            j += 1
        else:
            return None

    if j == len(pattern):
        return slots

    return None

def build_output(rule, slots):
    output = {}

    for k, v in rule["output"].items():
        if isinstance(v, str) and v.startswith("$"):
            slot_name = v[1:]
            output[k] = slots.get(slot_name)
        else:
            output[k] = v

    return output

def parse_with_grammar(text, category):
    tokens = normalize_tokens(text)

    for rule in GRAMMAR[category]:
        slots = match_pattern(tokens, rule)
        if slots is not None:
            return build_output(rule, slots)

    return None

if __name__ == '__main__':
    tests = [
        "create a 1/1 green saproling creature token",
        "create a 4/4 white angel creature token with flying",
        "draw two cards",
        "destroy target creature"
        ]
    
    for t in tests:
        print(t)
        o = parse_with_grammar(t, "EFFECT")
        if not o:
            print("FAILED")
        else:
            pprint(o)
        print()
    