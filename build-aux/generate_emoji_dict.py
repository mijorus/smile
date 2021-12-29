import csv
import json
import time 
import os
import requests
from problematic_emojis import problematic

emoji_list = json.load(open(os.path.dirname(__file__) + '/openmoji.json', 'r'))

output = []
cat = set()
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
    cat.add(el['group'])

print(f'emojis = {output}')
