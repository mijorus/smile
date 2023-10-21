import json

_active_localized_tags = {'lang': None, 'data': {}}

def get_localized_tags(lang: str, emoji_hexcode: str, datadir: str) -> list:
    global _active_localized_tags
    if _active_localized_tags['lang'] != lang:
        with open(file=datadir + f'/assets/emoji_locales/{lang}.json', mode='r') as f:
            _active_localized_tags = {'lang': lang, 'data': json.load(f)}

    if not emoji_hexcode in _active_localized_tags['data']:
        return []

    return _active_localized_tags['data'][emoji_hexcode]['tags']

def get_countries_list() -> dict:
        return {
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
            'ja': {
                'flag': '🇯🇵',
                'name': 'Japan',
                'language': 'Japanese',
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