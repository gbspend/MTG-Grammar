import json
import pickle

# https://mtgjson.com/downloads/all-files/#modern
with open('Modern.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

excl = ['availability','boosterTypes','borderColor','artist','artistIds','finishes','foreignData','identifiers','legalities','originalText','originalType','printings','purchaseUrls','rulings','skuIds','sourceProducts','uuid']

names = set()
cards = []
for s in data:
    for c in data[s]['cards']:
        n = c['name']
        if 'faceName' in c:
            n = c['faceName']
        if n not in names and 'paper' in c['availability']:
            for e in excl:
                if e in c:
                    del c[e]
            cards.append(c)
            names.add(n)

# 2. Convert and save as a Pickle file
with open('cards.pkl', 'wb') as f:
    pickle.dump(cards, f, protocol=pickle.HIGHEST_PROTOCOL)
