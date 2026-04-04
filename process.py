import re
import pickle
from pprint import pprint

types = {'Land', 'Instant', 'Creature', 'Sorcery', 'Planeswalker', 'Enchantment', 'Battle', 'Artifact', 'Kindred'}

def matchAll(l, boolf):
    return [e for e in l if boolf(e)]

def nonperm(c):
    return "Instant" in c['types'] or "Sorcery" in c['types']

q_abils = []

#of course, we can revisit any of these, likely to extract individual effects
matchexcl = ['{P}', '{H}', '{E}', " | ", "• "]

#return either:
#   generalized string ({4} -> {N} etc etc), OR
#   None if exclude
def generalize(s):
    global q_abils
    for e in matchexcl:
        if e in s:
            return None
    s = re.sub(r'\d+','N',s)
    s = s.replace("{Q}","{T}") #untap -> tap
    s = re.sub(r"\{[^T}]*\}","{M}",s) #{mana}
    s = re.sub(r"(\{M\})+","MANA", s)
    quot_re = r'"[^"]+"'
    while re.search(quot_re, s):
        q_abils.append(re.search(quot_re, s).group()[1:-1])
        s = re.sub(quot_re,"QUOTABIL",s,count=1)
    #last step: 2+ spaces -> 1 space
    s = re.sub("[ ]+"," ",s)
    return s

def allBeforeAfter(cards, sub):
    ret = []
    for c in cards:
        if "Saga" in c['type']:
            continue
        ret += beforeAfter(c['text'],sub)
    return ret

#return all snippets of s that match sub, extended to prev and post space char
def beforeAfter(s, sub):
    ret = []
    while s.find(sub) != -1:
        i = s.find(sub)
        j = i + len(sub)
        prei = 0
        posti = s.find(" ",j)
        if posti == -1:
            posti = len(s)
        ret.append(s[prei:posti])
        s = s[j:]
    return ret

with open('cards.pkl', 'rb') as file:
    cards = pickle.load(file)

#subset of cards to focus on
focus = []

costs = []
#things like:
#   <cost>:<effect>
#   When <trigger>, <effect>
effects = []

for c in cards:
    if 'text' not in c:
        continue
    t = generalize(c['text'])
    if t is None:
        continue
    c['text'] = t
    lines = c['text'].split("\n")
    for l in lines:
        i = l.find(":")
        if i == -1:
            continue
        cost = l[:i].strip()
        effect = l[i+1:].strip()
        costs.append(cost)
        effects.append(effect)
    c['lines'] = lines #TEMP?
    focus.append(c)


ci = set()
for s in costs:
    if " and " in s:
        continue
    for i in s.split(","):
        ci.add(i.strip())

    
#find all counter types...
cs = set([s.strip().replace("counters","counter").split("\n")[0].replace(".","") for s in c if "countered" not in s and "," not in s])