import re
import pickle
from pprint import pprint
import spacy

#this is findall for regex with groups
def groupFindAll(reg, s):
    out = []
    while True:
        match = re.search(reg,s)
        if not match:
            break
        out.append(match.group(0))
        s = s[match.end():]
    return out

# Load a small Eng  lish model (fast, good enough for normalization)
nlp = spacy.load("en_core_web_sm")
#text = "At the beginning of your end step, if you gained life this turn, create a 4/4 white Angel creature token with flying"
#doc = nlp(text)

types = {'Land', 'Instant', 'Creature', 'Sorcery', 'Planeswalker', 'Enchantment', 'Battle', 'Artifact', 'Kindred'}

ctypes = ["Advisor","Aetherborn","Alien","Ally","Angel","Antelope","Ape","Archer","Archon","Armadillo","Army","Artificer","Assassin","Assembly-Worker","Astartes","Atog","Aurochs","Avatar","Azra","Badger","Balloon","Barbarian","Bard","Basilisk","Bat","Bear","Beast","Beaver","Beeble","Beholder","Berserker","Bird","Bison","Blinkmoth","Boar","Bringer","Brushwagg","Camarid","Camel","Capybara","Caribou","Carrier","Cat","Centaur","Child","Chimera","Citizen","Cleric","Clown","Cockatrice","Construct","Coward","Coyote","Crab","Crocodile","C’tan","Custodes","Cyberman","Cyclops","Dalek","Dauthi","Demigod","Demon","Deserter","Detective","Devil","Dinosaur","Djinn","Doctor","Dog","Dragon","Drake","Dreadnought","Drix","Drone","Druid","Dryad","Dwarf","Echidna","Efreet","Egg","Elder","Eldrazi","Elemental","Elephant","Elf","Elves","Elk","Employee","Eye","Faerie","Ferret","Fish","Flagbearer","Fox","Fractal","Frog","Fungus","Gamer","Gargoyle","Germ","Giant","Gith","Glimmer","Gnoll","Gnome","Goat","Goblin","God","Golem","Gorgon","Graveborn","Gremlin","Griffin","Guest","Hag","Halfling","Hamster","Harpy","Hedgehog","Hellion","Hero","Hippo","Hippogriff","Homarid","Homunculus","Horror","Horse","Human","Hydra","Hyena","Illusion","Imp","Incarnation","Inkling","Inquisitor","Insect","Jackal","Jellyfish","Juggernaut","Kangaroo","Kavu","Kirin","Kithkin","Knight","Kobold","Kor","Kraken","Llama","Lamia","Lammasu","Leech","Lemur","Leviathan","Lhurgoyf","Licid","Lizard","Lobster","Manticore","Masticore","Mercenary","Merfolk","Metathran","Minion","Minotaur","Mite","Mole","Monger","Mongoose","Monk","Monkey","Moogle","Moonfolk","Mount","Mouse","Mutant","Myr","Mystic","Nautilus","Necron","Nephilim","Nightmare","Nightstalker","Ninja","Noble","Noggle","Nomad","Nymph","Octopus","Ogre","Ooze","Orb","Orc","Orgg","Otter","Ouphe","Ox","Oyster","Pangolin","Peasant","Pegasus","Pentavite","Performer","Pest","Phelddagrif","Phoenix","Phyrexian","Pilot","Pincher","Pirate","Plant","Platypus","Porcupine","Possum","Praetor","Primarch","Prism","Processor","Qu","Rabbit","Raccoon","Ranger","Rat","Rebel","Reflection","Rhino","Rigger","Robot","Rogue","Sable","Salamander","Samurai","Sand","Saproling","Satyr","Scarecrow","Scientist","Scion","Scorpion","Scout","Sculpture","Seal","Serf","Serpent","Servo","Shade","Shaman","Shapeshifter","Shark","Sheep","Siren","Skeleton","Skunk","Slith","Sliver","Sloth","Slug","Snail","Snake","Soldier","Soltari","Spawn","Specter","Spellshaper","Sphinx","Spider","Spike","Spirit","Splinter","Sponge","Squid","Squirrel","Starfish","Surrakar","Survivor","Symbiote","Synth","Tentacle","Tetravite","Thalakos","Thopter","Thrull","Tiefling","Toy","Treefolk","Trilobite","Triskelavite","Troll","Turtle","Tyranid","Unicorn","Vampire","Varmint","Vedalken","Villain","Volver","Wall","Walrus","Warlock","Warrior","Weasel","Weird","Werewolf","Whale","Wizard","Wolf","Wolverine","Wombat","Worm","Wraith","Wurm","Yeti","Zombie","Zubera"]

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
def generalize(s,c=None):
    global q_abils
    for e in matchexcl:
        if e in s:
            return None
    if c:
        s = s.replace(c['name'],"~")
        s = s.replace(c['name'].split(",")[0],"~")
        for ty in c['type'].replace("—","").split() + ["permanent", "spell","token"]:
            if ty.lower() in s.lower():
                s = re.sub(r"this "+ty,"~",s,flags=re.I)
    for ct in ctypes:
        if ct in s: #check before doing slow re.sub
            s = re.sub(r"\b"+ct+r"\b","CTYPE",s)
            s = re.sub(r"\b"+ct+r"s\b","CTYPE",s)
    s = re.sub(r"(CTYPE )+CTYPE","CTYPE",s)
    s = re.sub(r'\d+','N',s)
    for num in [
            "one","two","three","four","five","six","seven","eight","nine","ten",
            "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
            "eighteen", "nineteen", "twenty", "ninety-nine"
        ]:
        if num in s:
            s = re.sub(r"\b"+num+r"\b","N",s)
    for col in ["white","blue","black","red","green","colorless","multicolored"]:
        if col in s:
            s = re.sub(r"\b"+col+r"\b","COLOR",s)
    if "/" in s:
        s = re.sub(r"[XN]/[XN]","PT",s)
        s = re.sub(r"[+-]\w\/[+-]\w","PTMOD",s)
        #after this, only "/" left is "and/or"
    s = s.replace("{Q}","{T}") #untap -> tap
    s = re.sub(r"\{[^T}]*\}","{M}",s) #{mana}
    s = re.sub(r"(\{M\})+","MANA", s)
    s = s.replace(" an "," a ")
    s = s.replace(" another "," a ")
    quot_re = r'"[^"]+"'
    while re.search(quot_re, s):
        abil = re.search(quot_re, s).group()[1:-1]
        q_abils.append(abil)
        repl = "QUOTABIL"
        #if abil ends in period, add one after QUOTABIL
        if abil[-1] == ".":
            repl += "."
        s = re.sub(quot_re,repl,s,count=1)
    #last step: 2+ spaces -> 1 space
    s = re.sub("[ ]+"," ",s)
    return s

#== REAL TIME HELPERS =======================================================

def allBeforeAfter(cards, sub):
    ret = []
    for c in cards:
        if 'lines' not in c: #!
            continue
        for l in c['lines']:
            ret += beforeAfter(l,sub)
    return ret

#return all snippets of s that match sub, extended to prev and post space char
def beforeAfter(s, sub):
    ret = []
    while s.find(sub) != -1:
        i = s.find(sub)
        j = i + len(sub)
        prei = s.rfind(" ",0,i)
        if prei == -1:
            prei = 0
        posti = s.find(" ",j)
        if posti == -1:
            posti = len(s)
        ret.append(s[prei:posti])
        s = s[j:]
    return ret

#go through all card texts and return SET of reg matches
def matchSet(cards, reg, i = False):
    s = set()
    for c in cards:
        text = c['text']
        if not i:
            found = re.findall(reg, text)
        else:
            found = re.findall(reg, text, re.I)
        s.update(found)
    return s

#get list of all texts that include the substring
def matchSub(cards, sub):
    l = []
    for c in cards:
        text = c['text']
        if sub in text:
            l.append(text)
    return l

#== MAIN ===================================================================

if __name__ == "__main__":

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
        t = generalize(c['text'],c)
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



    #Working on costs
    ci = set()
    for s in costs:
        if " and " in s:
            continue
        for i in s.split(","):
            j = i.find(" — ")
            if j != -1:
                i = i[j+3:]
            ci.add(i.strip())



    for s in sorted(ci)[:10]:
        print(s)




    posts = set()
    for s in matchSet(focus, r"create[^.]+token[^.]*\.", True):
        i = s.find(" ")
        p = s[i+1:]
        if s[:i].lower() == "created":
            continue
        p = re.sub(r"([A-Z]{2,})(, \1)*,? (and|or) \1",r"\1",p)
        ALEG = ", a legendary "
        i = p.find(ALEG)
        if i != -1:
            p = "a "+p[i+len(ALEG):]
        posts.add(p)

    create = sorted(posts)

    for s in create[:10]:
        print(repr(s))





    #find all counter types...
    #c = allBeforeAfter(cards, " counter")
    #cs = set([s.strip().replace("counters","counter").split("\n")[0].replace(".","") for s in c if "countered" not in s and "," not in s])

