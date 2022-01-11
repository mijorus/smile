#!/usr/bin/env python3

import csv
import json
import time 
import os
from io import StringIO
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


output_dict = StringIO()
print(f'emojis = {output}', file=output_dict)

output_file = open(f"{os.path.dirname(__file__)}/../src/lib/emoji_list.py", 'w+')
output_file.write(output_dict.getvalue())

