import json
import re
import pickle

# https://mtgjson.com/downloads/all-files/#modern
# Oh, should use Modern Atomic instead...
with open('Modern.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

excl = ['availability','boosterTypes','borderColor','artist','artistIds','finishes','foreignData','identifiers','legalities','originalText','originalType','printings','purchaseUrls','rulings','skuIds','sourceProducts','uuid']

names = set()
cards = []
for s in data:
    for c in data[s]['cards']:
        if 'faceName' in c:
            c['name'] = c['faceName']
        n = c['name']
        if n not in names and 'paper' in c['availability'] and 'text' in c:
            for e in excl:
                if e in c:
                    del c[e]
            t = re.sub(r'\([^)]*\)', '', c['text']).strip()
            lines = []
            for s in t.split("\n"):
                s = s.strip()
                if not s:
                    continue
                lines.append(s)
            c['text'] = "\n".join(lines)
            cards.append(c)
            names.add(n)

with open('cards.pkl', 'wb') as f:
    pickle.dump(cards, f, protocol=pickle.HIGHEST_PROTOCOL)
