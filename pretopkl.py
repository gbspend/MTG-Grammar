from atomize import Atomizer
import json
import re
import pickle

# https://mtgjson.com/downloads/all-files/#modern
# Oh, should use Modern Atomic instead...
with open('Modern.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

EXCL = ['availability','boosterTypes','borderColor','artist','artistIds','finishes','foreignData','identifiers','legalities','originalText','originalType','printings','purchaseUrls','rulings','skuIds','sourceProducts','uuid']

#This is annoying, and MUCH WORSE for flavor words! >:(
#If card text has <i> (or w/e), this would be a single regex sub!
#   Issue submitted to mtgjson GitHub \crossfingers
ABIL_WS = ["Adamant", "Addendum", "Alliance", "Battalion", "Bloodrush", "Celebration", "Channel", "Chroma", "Cohort", "Constellation", "Converge", "Corrupted", "Council's dilemma", "Coven", "Delirium", r"Descend \d", "Domain", "Eerie", "Eminence", "Enrage", "Fateful Hour", "Fathomless descent", "Ferocious", "Flurry", "Formidable", "Grandeur", "Hellbent", "Heroic", "Imprint", "Inspired", "Join forces", "Kinship", "Landfall", "Lieutenant", "Magecraft", "Metalcraft", "Morbid", "Pack tactics", "Parade!", "Paradox", "Parley", "Radiance", "Raid", "Rally", "Renew", "Revolt", "Secret council", "Spell mastery", "Strive", "Survival", "Sweep", "Tempting offer", "Threshold", "Undergrowth", "Valiant", r"Will of the \w+"]

names = set()
cards = []
atomizer = Atomizer()
for s in data:
    for c in data[s]['cards']:
        if 'faceName' in c:
            c['name'] = c['faceName']
        n = c['name']
        if n not in names and 'paper' in c['availability'] and 'text' in c:
            for e in EXCL:
                if e in c:
                    del c[e]
            t = c['text']
            #remove parentheticals
            if "(" in t:
                t = re.sub(r'\([^)]*\)', '', t).strip()
            if '−' in t: #THIS IS NOT A HYPHEN, it's b'\xe2\x88\x92' (???)
                t = t.replace('−','-')
            #remove ability words
            if "—" in t:
                for aw in ABIL_WS:
                    aw = aw.lower()
                    if aw in t.lower():
                        t = re.sub(aw+' — ', '', t, flags=re.I).strip()
            #replace name with ~
            #   should handle legendary-first-name in text WITHOUT comma in name, IF
            #       that leg-1st-name is exactly everything before first space \shrug
            t = t.replace(c['name'],"~")
            if "Legendary" in c['type']:
                if "," in c['name']:
                    single_name = c['name'].split(",")[0].strip()
                else:
                    single_name = c['name'].split()[0].strip()
                t = t.replace(single_name,"~")
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
            atoms = []
            for l in lines:
                atoms.append(atomizer.tokenize(l))
            c['atoms'] = atoms
            c['text'] = "\n".join(lines)
            cards.append(c)
            names.add(n)

quotabils = sorted(atomizer.quotabils)
atomizer = Atomizer()
atom_abils = []
for s in quotabils:
    atom_abils.append(atomizer.tokenize(s))
#print("QUOTA-in-QUOTA:",len(atomizer.quotabils)) #currently 0 because don't match single quote

with open('cards.pkl', 'wb') as f:
    pickle.dump(cards, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('quotabils.pkl', 'wb') as f:
    pickle.dump(atom_abils, f, protocol=pickle.HIGHEST_PROTOCOL)

