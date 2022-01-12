#!/usr/bin/env python3

import csv
import json
import time 
import os
import subprocess
from io import StringIO
from problematic_emojis import problematic

emoji_list = json.load(open(os.path.dirname(__file__) + '/openmoji.json', 'r'))

output = {}
cat = set()

def append_skintone(skintone: dict, base_hex: str):
    global output
    for e, o in output.items():
        if o['hexcode'] == base_hex: 
            if not 'skintones' in o:
                o['skintones'] = []

            o['skintones'].append(skintone) 

for i, el in enumerate(emoji_list):
    if problematic.__contains__(el['hexcode']) or el['group'] == 'extras-openmoji':
        continue

    if el['unicode']:
        try:
            if float(el['unicode']) >= 11:
                continue
        except:
            pass

    if (len(el['skintone_base_hexcode']) > 0) and (el['skintone_base_hexcode'] != el['hexcode']):
        append_skintone(el, el['skintone_base_hexcode'])
        continue

    nested_groups = {
            'food-drink':  'animals-nature',
            'component':  'symbols',
            'symbols':  'objects',
            'people-body':  'smileys-emotion',
            'extras-unicode': 'symbols',
    }

    if el['group'] in nested_groups:
        el['group'] = nested_groups[el['group']]

    output[el['emoji']] = el
    cat.add(el['group'])


output_dict = StringIO()
print(f'emojis = {output}', file=output_dict)

output_file = open(f"{os.path.dirname(__file__)}/../src/lib/emoji_list.py", 'w+')
output_file.write(output_dict.getvalue())

subprocess.call(['python3', '-m', 'compileall', os.path.abspath(output_file.name)])