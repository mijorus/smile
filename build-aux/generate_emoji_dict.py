import csv
import json
import time 
import requests
from problematic_emojis import problematic

emoji_list = requests.get('https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/data/openmoji.json').json()

output = []
for i, el in enumerate(emoji_list):
    if problematic.__contains__(el['hexcode']) or el['group'] == 'extras-openmoji':
        continue

    if el['unicode']:
        try:
            if float(el['unicode']) >= 11:
                continue
        except:
            pass

    output.append(el)

print(f'emojis = {output}')
