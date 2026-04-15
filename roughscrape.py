#roughly, but accurately, scrape atomize.py for list of "atom" non-terminals

tags = set()

with open("atomize.py","r") as f:
    for line in f.readlines():
        if "atsub(" in line and "def atsub" not in line:
            parts = line.strip().split(",")
            #s = atsub(r'\d+','N',s,subs)
            #                 -3  -2 -1
            tag = parts[-3].strip()
            if '"' not in tag and "'" not in tag:
                print("non-quoted tag skipped:",tag)
                continue
            tags.add(tag[1:-1])

out = "["+(", ".join(sorted(tags)))+"]"
print(out)