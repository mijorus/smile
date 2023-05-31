import json
import requests
import os
from io import StringIO

problematic = [
    # Skin tones
    '1F3FB',
    '1F3FC',
    '1F3FD',
    '1F3FE',
    '1F3FF',

    # hair styles
    "1F9B0",
    "1F9B1",
    "1F9B3",
    "1F9B2",

    # duplicated USA flag
    "1F1FA-1F1F2"
]

output = {}

emoji_categories = {
    'recents': {
        'icon': 'history-undo-symbolic',
    },
    'smileys-emotion': {
        'icon': 'sentiment-very-satisfied-symbolic',
    },
    'animals-nature': {
        'icon': 'bear-symbolic'
    },
    'food-drink': {
        'icon': 'restaurant-symbolic'
    },
    'travel-places': {
        'icon': 'driving-symbolic'
    },
    'events': {
        'icon': 'birthday-symbolic'
    },
    'activities': {
        'icon': 'baseball-symbolic'
    },
    'objects': {
        'icon': 'lightbulb-symbolic'
    },
    'symbols': {
        'icon': 'input-keyboard-numlock-symbolic'
    },
    'flags': {
        'icon': 'flag-filled-symbolic'
    },
}

components = {}

def append_skintone(skintone: dict, base_hex: str):
    global output
    for e, o in output.items():
        if o['hexcode'] == base_hex:
            if 'skintones' not in o:
                o['skintones'] = []

            o['skintones'].append(skintone)

def main():
    _path = os.path.dirname(os.path.abspath(__file__))

    destdir = os.path.dirname(os.path.abspath(__file__)) + '/../../src/assets'

    categ = set()

    print('Downloading openmoji.json')
    openmoji_json = requests.get('https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/data/openmoji.json')

    with open(_path + '/openmoji.json', 'w+') as f:
        f.write(openmoji_json.text)

    emoji_list = json.load(open(_path + '/openmoji.json', 'r'))
    for i, el in enumerate(emoji_list):
        if el['group'] == 'component':
            if not el['subgroups'] in components:
                components[ el['subgroups'] ] = {}

            components[el['subgroups']][el['hexcode']] = el

        # ignore if an emoji is misbehaving
        
        if (el['hexcode'] in problematic) or (el['group'] == 'extras-openmoji'):
            continue

        if (len(el['skintone_base_hexcode']) > 0) and (el['skintone_base_hexcode'] != el['hexcode']):
            append_skintone(el, el['skintone_base_hexcode'])
            # skip if we already have the base emoji
            continue

        ignored_groups = ['extras-unicode']
        if ignored_groups.__contains__(el['group']):
            # ignore if the emoji belongs to the aforementioned groups because they create caos and look bad
            continue

        if 'flag:' in el['annotation']:
            el['annotation'] = el['annotation'].replace('flag:', '')
        elif ':' in el['annotation']:
            el['annotation'] = el['annotation'].split(':')[0]
        
        el['annotation'] = el['annotation'].strip()

        el['tags'] += f',{el["openmoji_tags"]}' if el["openmoji_tags"] else ''
        el['tags'] += f',{el["annotation"]}' if el["annotation"] else ''
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

        for useless_key in ["openmoji_tags", "openmoji_author", "openmoji_date", "annotation", "skintone_combination"]:
            if useless_key in el: 
                del el[useless_key]

        output[el['hexcode']] = el
        categ.add(el['group'])

    output_dict = StringIO()
    print(f'emojis = {output}\nemoji_categories = {emoji_categories}\ncomponents = {components}', file=output_dict)

    output_file = open(f"{destdir}/emoji_list.py", 'w+')
    output_file.write(output_dict.getvalue())

    print(f"Generated {destdir}/emoji_list.py")

if __name__ == '__main__':
    main()
