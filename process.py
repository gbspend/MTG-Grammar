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

def processAll():
    with open('cards.pkl', 'rb') as file:
        cards = pickle.load(file)
    
    with open('quotabils.pkl', 'rb') as file:
        quotabils = pickle.load(file)


    grammar = gram2obj.load("grammar.txt")

    N = 100
    total = 0
    done = 0
    part = 0
    all_items = []
    #untouched = []
    #put in common format so can parse w/ same loop
    cards_n_abils = [(c['atoms'],c) for c in cards] + [(quotabils,None)]
    for atoms, c in cards_n_abils:
        parsed = []
        for old_tok, old_sub in atoms:
            tokens, subs = parse.parse(grammar,old_tok, old_sub)
            parsed.append((tokens,subs))
            total += 1
            if len(old_tok) > len(tokens):
                part += 1
                if all_parsed(tokens):
                    done += 1
                    #print(line)
                    #print(old_tok)
                    #print(tokens)
                    #pprint(subs)
                    #print()
            #else: #not useful?
            #    untouched.append(i)
        all_items += parsed
        if c:
            c['parsed'] = parsed #keep in card context!

    print("Total:",total)
    print_percent("Done: ",done,total)
    print_percent("Part: ",part,total)
    #TODO collate and report failures/partials AND false positives! BUT HOW???

    '''
    for t,s in all_items[:10]:
        print(t)
        pprint(s)
        print()
    '''
    print("CARDS LEN:  ",len(cards))
    print("ALL_ITS LEN:",len(all_items))
    
    pts = {}
    for supertok in ["COST","EFFECT","TRIG","POST_TRIG"]:
        if supertok not in pts:
            pts[supertok] = PatternTree()
        #look for patterns!
        #   TODO: also look in subs, esp. * rules
        for toks, subs in all_items:
            for tok,s in subs:
                if tok == supertok:
                    pts[supertok].addToks(atomize.smart_split(s))
    
    return all_items, pts

def mostRec(curr,depth,tabs):
    ts = "  "*tabs
    if depth > 0:
        print(curr.s)
        if curr.children:
            end_at_curr = curr.count - sum(n.count for n in curr.children)
            for child in sorted(
                curr.children+[curr],
                key=lambda n:end_at_curr if n == curr else n.count,
                reverse=True
                ):
                if child.count == 1:
                    continue
                if child == curr:
                    if end_at_curr > 0:
                        print(ts+"|")
                        print(ts+str(end_at_curr)+"--> STOP")
                else:
                    print(ts+"|")
                    print(ts+str(child.count)+"--> ",end="")
                    mostRec(child,depth-1,tabs+1)
    else:
        print(mosts(curr)+" [...]")
            

def mosts(curr):
    out = []
    while True:
        out.append(curr.s)
        if not curr.children:
            break
        end_at_curr = curr.count - sum(n.count for n in curr.children)
        curr = sorted(curr.children, key=lambda n:n.count, reverse=True)[0]
        #calculate how many strings end at current node; if that's greater
        #   than sum of all child counts, we stop here
        if curr.count == 1 or end_at_curr > curr.count:
            break
    return " ".join(out)

if __name__ == "__main__":
    all_items, pts = processAll()
    pt = pts["COST"]
    
    #print("COST")
    #mostRec(pt.root,3,0)
    
    candidates = sorted(pt.root.children, key=lambda n:n.count, reverse=True)
    m = candidates[0]
    print("MANA\n|")
    mostRec(m.children[0],100000,0)
    
    exit()
    print(pt.root.mosts())
    print()
    
    candidates = sorted(pt.root.children, key=lambda n:n.count, reverse=True)
    for n in candidates[:20]:
        print(n.s)


'''

from process import processAll, mostRec
all_items, pts = processAll()
pt = pts["COST"]
candidates = sorted(pt.root.children, key=lambda n:n.count, reverse=True)
print(len(candidates))
for n in candidates[:20]:
    print(n.s)


'''
#TODO:
#   separate effects... COST : EFFECT; TRIGGER , EFFECT; <non-permanent> EFFECT
#       -likely outside of grammar...
#   go back and parse COSTs, QUOTABILs, etc.

