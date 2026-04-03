from pprint import pprint
import pickle

def matchAll(cards, boolf):
    return [c for c in cards if boolf(c)]

with open('cards.pkl', 'rb') as file:
    cards = pickle.load(file)

zy = matchAll(cards, lambda c: "yae Ga" in c['name'])
pprint(zy)
