# this was used to scrape data from wikipedia

import requests

S = requests.Session()

URL = "https://tr.wiktionary.org/w/api.php"

PARAMS = {
    "action": "query",
    "cmtitle": "Category:Türkçe_adlar",
    "cmlimit": "500",
    "list": "categorymembers",
    "format": "json",
    "cmcontinue": "",
}
PAGES = []
while True:
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES += [x for x in DATA['query']['categorymembers']]
    if "continue" not in DATA:
        break
    PARAMS['cmcontinue'] = DATA['continue']['cmcontinue']

f = open("data/adlar.txt", "w", encoding="utf-8")
f.writelines([page["title"] + "\n" for page in PAGES])
