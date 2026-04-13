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
            #remove parentheticals
            t = re.sub(r'\([^)]*\)', '', c['text']).strip()
            #replace name with ~
            #   TODO: doesn't handle legendary-first-name in text WITHOUT comma in name:
            #           is:commander -name:"," o:~
            t = t.replace(c['name'],"~")
            if "Legendary" in c['type']:
                t = t.replace(c['name'].split()[0],"~")
            for ty in c['type'].replace("—","").split() + ["permanent", "spell","token"]:
                ty = ty.strip()
                if not ty:
                    continue
                if ty.lower() in t.lower():
                    t = re.sub(r"this "+ty,"~",t,flags=re.I)
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
