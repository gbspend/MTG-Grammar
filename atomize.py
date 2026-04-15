#BREAKTHROUGH: "atom" non-terminals can be processed programatically!
#	More flexibile than with grammar, AND...
#	Will preserve the literal(s) that were replaced with the atom

import re

CTYPES = ["Advisor","Aetherborn","Alien","Ally","Angel","Antelope","Ape","Archer","Archon","Armadillo","Army","Artificer","Assassin","Assembly-Worker","Astartes","Atog","Aurochs","Avatar","Azra","Badger","Balloon","Barbarian","Bard","Basilisk","Bat","Bear","Beast","Beaver","Beeble","Beholder","Berserker","Bird","Bison","Blinkmoth","Boar","Bringer","Brushwagg","Camarid","Camel","Capybara","Caribou","Carrier","Cat","Centaur","Child","Chimera","Citizen","Cleric","Clown","Cockatrice","Construct","Coward","Coyote","Crab","Crocodile","C’tan","Custodes","Cyberman","Cyclops","Dalek","Dauthi","Demigod","Demon","Deserter","Detective","Devil","Dinosaur","Djinn","Doctor","Dog","Dragon","Drake","Dreadnought","Drix","Drone","Druid","Dryad","Dwarf","Echidna","Efreet","Egg","Elder","Eldrazi","Elemental","Elephant","Elf","Elves","Elk","Employee","Eye","Faerie","Ferret","Fish","Flagbearer","Fox","Fractal","Frog","Fungus","Gamer","Gargoyle","Germ","Giant","Gith","Glimmer","Gnoll","Gnome","Goat","Goblin","God","Golem","Gorgon","Graveborn","Gremlin","Griffin","Guest","Hag","Halfling","Hamster","Harpy","Hedgehog","Hellion","Hero","Hippo","Hippogriff","Homarid","Homunculus","Horror","Horse","Human","Hydra","Hyena","Illusion","Imp","Incarnation","Inkling","Inquisitor","Insect","Jackal","Jellyfish","Juggernaut","Kangaroo","Kavu","Kirin","Kithkin","Knight","Kobold","Kor","Kraken","Llama","Lamia","Lammasu","Leech","Lemur","Leviathan","Lhurgoyf","Licid","Lizard","Lobster","Manticore","Masticore","Mercenary","Merfolk","Metathran","Minion","Minotaur","Mite","Mole","Monger","Mongoose","Monk","Monkey","Moogle","Moonfolk","Mount","Mouse","Mutant","Myr","Mystic","Nautilus","Necron","Nephilim","Nightmare","Nightstalker","Ninja","Noble","Noggle","Nomad","Nymph","Octopus","Ogre","Ooze","Orb","Orc","Orgg","Otter","Ouphe","Ox","Oyster","Pangolin","Peasant","Pegasus","Pentavite","Performer","Pest","Phelddagrif","Phoenix","Phyrexian","Pilot","Pincher","Pirate","Plant","Platypus","Porcupine","Possum","Praetor","Primarch","Prism","Processor","Qu","Rabbit","Raccoon","Ranger","Rat","Rebel","Reflection","Rhino","Rigger","Robot","Rogue","Sable","Salamander","Samurai","Sand","Saproling","Satyr","Scarecrow","Scientist","Scion","Scorpion","Scout","Sculpture","Seal","Serf","Serpent","Servo","Shade","Shaman","Shapeshifter","Shark","Sheep","Siren","Skeleton","Skunk","Slith","Sliver","Sloth","Slug","Snail","Snake","Soldier","Soltari","Spawn","Specter","Spellshaper","Sphinx","Spider","Spike","Spirit","Splinter","Sponge","Squid","Squirrel","Starfish","Surrakar","Survivor","Symbiote","Synth","Tentacle","Tetravite","Thalakos","Thopter","Thrull","Tiefling","Toy","Treefolk","Trilobite","Triskelavite","Troll","Turtle","Tyranid","Unicorn","Vampire","Varmint","Vedalken","Villain","Volver","Wall","Walrus","Warlock","Warrior","Weasel","Weird","Werewolf","Whale","Wizard","Wolf","Wolverine","Wombat","Worm","Wraith","Wurm","Yeti","Zombie","Zubera"]

def sub_split(parts,ch):
    ret = []
    for p in parts:
        if ch not in p:
            ret.append(p)
        else:
            sub = p.split(ch)
            ret.append(sub[0])
            for s in sub[1:]:
                ret.append(ch)
                if s: ret.append(s)
    return ret

def smart_split(s):
    syms = [",",".",":",'"']
    parts = s.split()
    for ch in syms:
        parts = sub_split(parts,ch)
    #pull punct out of quotes by swapping ..., '.', '"', ...
    #unnecessary after all?
    for i in range(len(parts)-1):
        if parts[i+1] == '"' and (parts[i] == ',' or parts[i] == '.'):
            temp = parts[i]
            parts[i] = parts[i+1]
            parts[i+1] = temp
    return parts

#"atomic regex sub"
def atsub(reg,name,s, subs):
    while re.search(reg, s):
        text = re.search(reg, s).group()
        subs.append((name,text))
        s = re.sub(reg,name,s,count=1)
    return s

NUMS = [
    "one","two","three","four","five","six","seven","eight","nine","ten",
    "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
    "eighteen", "nineteen", "twenty", "ninety-nine"
]

COLORS = ["white","blue","black","red","green","colorless","multicolored"]
COLORS += [s[0].upper()+s[1:] for s in COLORS]

#CHALLENGE: regex matching mutually excludes tokenized (smart_split) parsing... :(
#   tokenized makes it easier to keep track of replaced text (which old generalize DOESN'T do)
#   can I square the circle? ...
#       atsub will replace with name and return list of replaced texts \+1
#       but how to keep track of which "replaced"s match which name? ~maybe not too bad, BUT:
#       what about replacements of replacesments!?!? e.g. 4/4 -> N/N -> PT @_@
#   wait, order helps, right? ...right?
#       if you keep all of the "replaced"s in an ordered list and
#       work BACKWARDS through it to undo it..? yes? right?
#   try it for now

class Atomizer:
    def __init__(self):
        self.quotabils = set()

    #ALL ATOMIC non-terms must go here!
    def atomize(self, s):
        #DO THIS FIRST, then all QUOTABILs are raw instead of partially processed!
        #   NOTE: CANNOT add single quote bc would match: ...doesn't untap during its controller's...
        quot_re = r'"[^"]+"'
        while re.search(quot_re, s):
            print(s)
            abil = re.search(quot_re, s).group()[1:-1]
            repl = "QUOTABIL"
            #if abil ends in period or comma, add one after QUOTABIL
            last = abil[-1]
            if last == "." or last == ",":
                repl += last
                abil = abil[:-1]
            self.quotabils.add(abil)
            print(abil)
            s = re.sub(quot_re,repl,s,count=1)
            print()
        subs = []
        for ct in CTYPES:
            if ct in s: #check before doing slow re.sub
                s = atsub(r"\b"+ct+r"\b","CTYPE",s,subs)
                s = atsub(r"\b"+ct+r"s\b","CTYPE",s,subs)
        s = atsub(r"(CTYPE )+CTYPE","CTYPE",s,subs)
        s = atsub(r'\d+','N',s,subs)
        for num in NUMS:
            if num in s:
                s = atsub(r"\b"+num+r"\b","N",s,subs)
        for col in COLORS:
            if col in s:
                s = atsub(r"\b"+col+r"\b","COLOR",s,subs)
        if "/" in s:
            s = atsub(r"[XN]/[XN]","PT",s,subs)
        if "/" in s:
            s = atsub(r"[+-]\w\/[+-]\w","PTMOD",s,subs)
            #after this, only "/" left is "and/or"
        #s = s.replace("{Q}","{T}") #untap -> tap
        s = atsub(r"\{[^TM}]*\}","{M}",s,subs) #{mana}
        s = atsub(r"(\{M\})+","MANA",s,subs)
        #s = s.replace(" an "," a ")
        #s = s.replace(" another "," a ")
        #last step: 2+ spaces -> 1 space
        s = re.sub("[ ]+"," ",s)
        return s, subs

    def tokenize(self, text):
        text,subs = self.atomize(text)
        tokens = smart_split(text)
        return tokens,subs