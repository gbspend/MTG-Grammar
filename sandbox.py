from pprint import pprint
import pickle
with open('cards.pkl', 'rb') as file:
    cards = pickle.load(file)

def printCard(cards,name):
    for c in cards:
        if name in c['name']:
            pprint(c)
            print()

H = '—'
before = set()

for c in cards:
    for line in c['text'].split("\n"):
        c = line.count(H)
        if c > 1:
            pass#print("2+:",line)
        elif c == 1:
            before.add(line.split(H)[0].strip())


pre_no_sp = set()
import re
for c in cards:
    for t in c['text'].split("\n"):
        if H in t and re.search(r"[^\d \t\r\n]—[^\d \t\r\n]",t):
            t = re.sub(r"[X\d]+","N",t)
            parts = t.split(H)
            pre = parts[0].strip()
            if '"' in pre:
                continue #this would be separated by QUOTE_ABIL handler in real parser
            if pre not in pre_no_sp:
                print(t)
            pre_no_sp.add(pre)

pns = sorted(pre_no_sp,key=lambda s:len(s))
for s in pns:
    print(s)




#This finds abilities with abil-dash-cost, with NO SPACES around dash:
'''
Ward
Warp
Echo
Blitz
Morph
Evoke
Equip
Bestow
Escape
Kicker
Recover
Madness
Entwine
Buyback
Modular
Cycling
Escalate
Flashback
Suspend N
Replicate
Eternalize
Freerunning
Reinforce N
Chaosbringer
Cumulative upkeep
Splice onto Arcane
'''