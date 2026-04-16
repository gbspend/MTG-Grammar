import requests
from bs4 import BeautifulSoup

base = "https://mtg.wiki"

def parsePage(rel):
    response = requests.get(base+rel)
    soup2 = BeautifulSoup(response.content, "html.parser")
    table = soup2.find("table", {'class':['infobox','mainbox']})
    tbody = next(table.children)
    #TODO parse table rows looking for "Type" and "Reminder Text"
    
# Step 1: Fetch the HTML content from the URL
start = "/page/Keyword_ability"
response = requests.get(base+start)

# Step 2: Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

boxes = soup.findAll(True, {'class':['crDiv','crBox']})
topu = boxes[2].find('ul')
u = topu.find('ul')
i = 0
for t in u.children:
    a = t.find('a')
    if not a or a == -1:
        continue
    #parsePage(a['href'])
    print(a['href'])
    i += 1
    if i > 10:
        break

