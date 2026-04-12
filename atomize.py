#BREAKTHROUGH: "atom" non-terminals can be processed programatically!
#	More flexibile than with grammar, AND...
#	Will preserve the literal(s) that were replaced with the atom

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
    ret = []
    parts = s.split()
    for ch in syms:
        parts = sub_split(parts,ch)
    #pull punct out of quotes by swapping ..., '.', '"', ...
    for i in range(len(parts)-1):
        if parts[i+1] == '"' and (parts[i] == ',' or parts[i] == '.'):
            temp = parts[i]
            parts[i] = parts[i+1]
            parts[i+1] = temp
    return parts

#"atomic regex sub"
def atsub(reg,name,s):
    atoms = []
    while re.search(reg, s):
        text = re.search(reg, s).group()
        atoms.append(text)
        s = re.sub(reg,name,s,count=1)
    return s, atoms

#CHALLENGE: regex parsing mutually excludes tokenized parsing... :(
#   tokenized makes it easier to keep track of replaced text (which old generalize DOESN'T do)
#   can I square the circle? ...
#       atsub will replace with name and return list of replaced texts \+1
#       but how to keep track of which "replaced"s match which name? ~maybe not too bad, BUT:
#       what about replacements of replacesments!?!? e.g. 4/4 -> N/N -> PT @_@
def atomize(s):
    
    #TODO: change ALL OF THIS to use atsub instead
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