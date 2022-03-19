#!/usr/bin/env python3

import json
import os
import subprocess
from io import StringIO
from problematic_emojis import problematic

output = {}

def append_skintone(skintone: dict, base_hex: str):
    global output
    for e, o in output.items():
        if o['hexcode'] == base_hex:
            if 'skintones' not in o:
                o['skintones'] = []

            o['skintones'].append(skintone)

def main():
    prefix = os.environ.get('MESON_INSTALL_PREFIX', '/usr/local')
    datadir = os.path.join(prefix, 'share/smile/smile/assets')
    cat = set()

    emoji_categories = {
        'recents': {
            'icon': '🕖️',
        },
        'smileys-emotion': {
            'icon': '😀',
        },
        'animals-nature': {
            'icon': '🐶'
        },
        'food-drink': {
            'icon': '🍔'
        },
        'travel-places': {
            'icon': '🚘️'
        },
        'events': {
            'icon': '🎁'
        },
        'activities': {
            'icon': '⚽️'
        },
        'objects': {
            'icon': '💡'
        },
        'symbols': {
            'icon': '1️⃣'
        },
        'flags': {
            'icon': '🏳️'
        },
    }

    emoji_list = json.load(open(os.path.dirname(__file__) + '/openmoji.json', 'r'))
    for i, el in enumerate(emoji_list):
        # ignore if an emoji is misbehaving
        if problematic.__contains__(el['hexcode']) or el['group'] == 'extras-openmoji':
            continue

        if (len(el['skintone_base_hexcode']) > 0) and (el['skintone_base_hexcode'] != el['hexcode']):
            append_skintone(el, el['skintone_base_hexcode'])
            # skip if we already have the base emoji
            continue

        ignored_groups = ['extras-unicode']
        if ignored_groups.__contains__(el['group']):
            # ignore if the emoji belongs to the aforementioned groups because they create caos and look bad
            continue

        el['annotation'] = '' if (not el['annotation'].__contains__('flag')) else el['annotation'].replace('flag:', '').replace(' ', ',')

        el['tags'] = el["tags"]
        el['tags'] += f',{el["openmoji_tags"]}' if len(el["openmoji_tags"]) else ''
        el['tags'] += f',{el["annotation"]}' if len(el["annotation"]) else ''
        el['tags'] = el["tags"].replace('“', '').replace('”', '')

        # re-order groups
        nested_groups = {
            'component': 'symbols',
            'people-body': 'smileys-emotion',
            'extras-unicode': 'symbols',
        }

        if el['group'] in nested_groups:
            el['group'] = nested_groups[el['group']]

        # re-order subgroups
        subgroups = {
            'sky-weather': 'animals-nature',
            'time': 'objects',
            'event': 'events',
        }

        if el['subgroups'] in subgroups:
            el['group'] = subgroups[el['subgroups']]

        output[el['hexcode']] = el
        cat.add(el['group'])

    output_dict = StringIO()
    print(f'emojis = {output}\nemoji_categories = {emoji_categories}', file=output_dict)

    output_file = open(f"{datadir}/emoji_list.py", 'w+')
    output_file.write(output_dict.getvalue())

    subprocess.call(['python3', '-m', 'compileall', os.path.abspath(output_file.name)])

main()