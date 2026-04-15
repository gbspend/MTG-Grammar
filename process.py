import atomize
import gram2obj
import parse
from patterntree import PatternTree
import pickle
from pprint import pprint

def all_parsed(tokens):
    for tok in tokens:
        if tok == "." or tok == ",":
            continue
        if not parse.isNonTerm(tok):
            return False
    return True

def print_percent(name, n, total):
    p = (n/total) * 100
    print(name,n,f"({p:.2f}%)")

if __name__ == "__main__":
    with open('cards.pkl', 'rb') as file:
        cards = pickle.load(file)

    grammar = gram2obj.load("grammar.txt")

    N = 100
    total = 0
    done = 0
    part = 0
    items = []
    untouched = [] #indices into cards
    for i in range(len(cards)):
        c = cards[i]
        for old_tok, old_sub in c['atoms']:
            tokens, subs = parse.parse(grammar,old_tok, old_sub)
            total += 1
            if len(old_tok) > len(tokens):
                items.append((tokens,subs))
                part += 1
                if all_parsed(tokens):
                    done += 1
                    #print(line)
                    #print(old_tok)
                    #print(tokens)
                    #pprint(subs)
                    #print()
            else:
                untouched.append(i)

    print("Total:",total)
    print_percent("Done: ",done,total)
    print_percent("Part: ",part,total)
    #TODO collate and report failures/partials AND false positives! BUT HOW???

    '''
    for t,s in items[:10]:
        print(t)
        pprint(s)
        print()
    '''

    pt = PatternTree()
    #look for patterns!
    #   TODO: also look in subs, esp. * rules
    for i in untouched:
        c = cards[i]
        for toks, subs in c['atoms']:
            pt.addToks(toks)

    candidates = sorted(pt.root.children, key=lambda n:n.count, reverse=True)
    for n in candidates[:20]:
        print(n.s)

    #TODO:
    #   separate effects... COST : EFFECT; TRIGGER , EFFECT; <non-permanent> EFFECT
    #       -likely outside of grammar...
    #   go back and parse COSTs, QUOTABILs, etc.

