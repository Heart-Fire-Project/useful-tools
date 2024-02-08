import json

input_file = "origin.json"
output_file = "extracted.json"

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = {item['key']: item['translation'] for item in data}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)