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
                'name': 'Deutschland',
                'language': 'German',
            },
            'es': {
                'flag': '🇪🇸',
                'name': 'España',
                'language': 'Spanish',
            },
            'et': {
                'flag': '🇪🇪',
                'name': 'Eesti',
                'language': 'Estonian',
            },
            'fi': {
                'flag': '🇫🇮',
                'name': 'Suomi',
                'language': 'Finnish',
            },
            'fr': {
                'flag': '🇫🇷',
                'name': 'France',
                'language': 'French',
            },
            'hu': {
                'flag': '🇭🇺',
                'name': 'Magyarország',
                'language': 'Hungarian',
            },
            'it': {
                'flag': '🇮🇹',
                'name': 'Italia',
                'language': 'Italian',
            },
            'ja': {
                'flag': '🇯🇵',
                'name': '日本',
                'language': 'Japanese',
            },
            'ko': {
                'flag': '🇰🇷',
                'name': '대한민국',
                'language': 'Korean',
            },
            'ms': {
                'flag': '🇲🇴',
                'name': 'Malaysia',
                'language': 'Malay',
            },
            'nb': {
                'flag': '🇳🇴',
                'name': 'Norge',
                'language': 'Norwegian',
            },
            'nl': {
                'flag': '🇳🇱',
                'name': 'Nederland',
                'language': 'Dutch',
            },
            'pl': {
                'flag': '🇵🇱',
                'name': 'Polska',
                'language': 'Polish',
            },
            'pt': {
                'flag': '🇵🇹',
                'name': 'Portugal',
                'language': 'Portuguese',
            },
            'ru': {
                'flag': '🇷🇺',
                'name': 'Россия',
                'language': 'Russian',
            },
            'sv': {
                'flag': '🇸🇪',
                'name': 'Sverige',
                'language': 'Swedish',
            },
            'th': {
                'flag': '🇹🇭',
                'name': 'ไทย',
                'language': 'Thai',
            },
            'zh': {
                'flag': '🇨🇳',
                'name': '中国',
                'language': 'Chinese',
            },
        }