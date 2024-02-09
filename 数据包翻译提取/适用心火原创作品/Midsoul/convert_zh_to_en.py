# -*- coding: UTF-8 -*-
import json

input_file = "zh_cn.json"
output_file = "en_us.json"

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for key in list(data.keys()):
    if key.endswith('.cn'):
        new_key = key.replace('.cn', '.en')
        data[new_key] = data[key]
        data[key] = ""

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)