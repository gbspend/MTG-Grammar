from bs4 import BeautifulSoup
import pickle
import re
import requests

base = "https://mtg.wiki"

def parsePage(rel):
    response = requests.get(base+rel)
    soup2 = BeautifulSoup(response.content, "html.parser")
    table = soup2.find("table", {'class':['infobox','mainbox']})
    tbody = next(table.children)
    typ = ""
    rem = ""
    for t in tbody.children:
        th = t.find("th")
        if not th:
            continue
        if th.text == "Type":
            a = t.find("a")
            if a:
                typ = a.text
        if th.text == 'Reminder Text':
            r = t.find("td")
            if r:
                #remove all tags, leaving text
                for tag in r.find_all():
                    tag.decompose()
                raw_rem = r.text.strip() #cut out pre and post td
                rem = [s.strip() for s in raw_rem.split("  ") if s] #can we count on splitting on "  "?
    return typ, rem        


# Step 1: Fetch the HTML content from the URL
start = "/page/Keyword_ability"
response = requests.get(base+start)

# Step 2: Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

boxes = soup.findAll(True, {'class':['crDiv','crBox']})
topu = boxes[2].find('ul')
u = topu.find('ul')
i = 0

all_abils = {}
for t in u.children:
    a = t.find('a')
    if not a or a == -1:
        continue
    h = a['href']
    name = h.split("/")[-1]
    res = parsePage(h)
    all_abils[name] = res

with open('keywords.pkl', 'wb') as f:
    pickle.dump(all_abils, f, protocol=pickle.HIGHEST_PROTOCOL)


'''

import pickle
with open('keywords.pkl', 'rb') as file:
    all_abils = pickle.load(file)

'''