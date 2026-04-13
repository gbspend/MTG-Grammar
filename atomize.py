#BREAKTHROUGH: "atom" non-terminals can be processed programatically!
#	More flexibile than with grammar, AND...
#	Will preserve the literal(s) that were replaced with the atom

from process import ctypes #move to here?
import re

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

#ALL ATOMIC non-terms must go here!
def atomize(s):
    subs = []
    #TODO: change ALL OF THIS to use atsub instead
    for ct in ctypes:
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
    s = atsub(r"\{[^T}]*\}","{M}",s,subs) #{mana}
    s = atsub(r"(\{M\})+","MANA",s,subs)
    #s = s.replace(" an "," a ")
    #s = s.replace(" another "," a ")
    quot_re = r'"[^"]+"'
    while re.search(quot_re, s):
        abil = re.search(quot_re, s).group()[1:-1]
        q_abils.append(abil)
        repl = "QUOTABIL"
        #if abil ends in period, add one after QUOTABIL
        if abil[-1] == "." or abil[-1] == ",":
            repl += abil[-1]
        s = re.sub(quot_re,repl,s,count=1)
    #last step: 2+ spaces -> 1 space
    s = re.sub("[ ]+"," ",s)
    return s, subs