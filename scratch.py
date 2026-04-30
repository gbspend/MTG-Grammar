import pickle
with open('keywords.pkl', 'wb') as f:
    pickle.dump(all_abils, f, protocol=pickle.HIGHEST_PROTOCOL)



import pickle
with open('keywords.pkl', 'rb') as file:
    all_abils = pickle.load(file)



from pprint import pprint
import pickle
with open('quotabils.pkl', 'rb') as file:
    quotabils = pickle.load(file)



from pprint import pprint
import pickle
with open('cards.pkl', 'rb') as file:
    cards = pickle.load(file)


for c in cards:
    if c['name'] == "Splash Portal":
        pprint(c)



t1 = "CTYPE, CTYPE, CTYPE,"
done = False
for c in cards:
    if done:
        break
    for s,subs in c['atoms']:
        if done:
         break
        for tok,sub in subs:
            if t1 in sub:
                pprint(c)
                done = True
                break


from process import processAll
all_items, pts = processAll()
loy = set()
for tok,sub in all_items:
    if not sub:
            continue
    for s in sub:
            if s[0] == "LOY":
                    loy.add(s[1])


loy
