import csv
import json
import time 
import requests


emoji_list = requests.get('https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/data/openmoji.csv').text

reader = csv.reader(emoji_list.splitlines())

output = []
headers = []
for i, row in enumerate(reader):
    if i == 0:
        headers = row
    else:
        emoji = {}
        for j, col in enumerate(row):
            emoji[headers[j]] = col

        output.append(emoji)

print(f'emojis = {output}')
