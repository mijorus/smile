#
# This script was developed with the only purpose of getting the list of locales
# from emojibase's CDN.
# 
# I'll leave the code here if it will ever need to be used again.
# 

# import requests
# import json

# def main():
#     locales = [
#         'da',
#         'de',
#         'en',
#         'es',
#         'et',
#         'fi',
#         'fr',
#         'hu',
#         'it',
#         'ja',
#         'ko',
#         'lt',
#         'ms',
#         'nb',
#         'nl',
#         'pl',
#         'pt',
#         'ru',
#         'sv',
#         'th',
#         'uk',
#         'zh',
#     ]

#     for locale in locales:
#         print(f'Getting {locale}')
#         r = requests.get(f'https://cdn.jsdelivr.net/npm/emojibase-data@latest/{locale}/data.json')
        
#         output = {}
#         for emoji in r.json():
#             if 'tags' in emoji:
#                 output[emoji['hexcode']] = {
#                     'tags': emoji['tags'],
#                 }

#         with open(f'{locale}.json', 'w+') as f:
#             f.write(json.dumps(output))

# if __name__ == '__main__':
#     main()