
## This script was developed with the only purpose of getting the list of locales
## from emojibase's CDN.
##
## I'll leave the code here if it will ever need to be used again.


import requests
import json
import os

def main():
    _path = os.path.dirname(os.path.abspath(__file__))

    locales = {
            'da': {
                'flag': '🇩🇰',
                'name': 'Danmark',
                'language': 'Danish',
            },
            'de': {
                'flag': '🇩🇪',
                'name': 'Germany',
                'language': 'German',
            },
            'es': {
                'flag': '🇪🇸',
                'name': 'Spain',
                'language': 'Spanish',
            },
            'et': {
                'flag': '🇪🇪',
                'name': 'Estonia',
                'language': 'Estonian',
            },
            'fi': {
                'flag': '🇫🇮',
                'name': 'Finland',
                'language': 'Finnish',
            },
            'fr': {
                'flag': '🇫🇷',
                'name': 'France',
                'language': 'French',
            },
            'hu': {
                'flag': '🇭🇺',
                'name': 'Hungary',
                'language': 'Hungarian',
            },
            'it': {
                'flag': '🇮🇹',
                'name': 'Italy',
                'language': 'Italian',
            },
            'nb': {
                'flag': '🇳🇴',
                'name': 'Norway',
                'language': 'Norwegian',
            },
            'nl': {
                'flag': '🇳🇱',
                'name': 'Nederland',
                'language': 'Dutch',
            },
            'pl': {
                'flag': '🇵🇱',
                'name': 'Poland',
                'language': 'Polish',
            },
            'pt': {
                'flag': '🇵🇹',
                'name': 'Portugal',
                'language': 'Portuguese',
            },
            'ru': {
                'flag': '🇷🇺',
                'name': 'Russia',
                'language': 'Russian',
            },
            'sv': {
                'flag': '🇸🇪',
                'name': 'Sweden',
                'language': 'Swedish',
            }
        }

    for locale, locale_obj in locales.items():
        print('loading: ' + locale)
        r = requests.get(f'https://cdn.jsdelivr.net/npm/emojibase-data@latest/{locale}/data.json')
        
        output = {}
        for emoji in r.json():
            if 'tags' in emoji:
                output[emoji['hexcode']] = {
                    'tags': emoji['tags'],
                    'emoji': emoji['emoji'],
                }

        with open(f'{_path}/../../data/assets/emoji_locales/{locale}.json', 'w+') as f:
            # json pretty print
            f.write(json.dumps(output, indent=4, sort_keys=True, ensure_ascii=False))

if __name__ == '__main__':
    main()