import os
import json
import re
from jsonfinder import jsonfinder

directory = "data/"
output_file = "data/text/text.json"
result = {}


def process_json_object(json_object, result):
    if isinstance(json_object, dict):
        text = json_object.get("text")
        if text and text not in result:
            result[text] = text


def process_mcfunction_file(filepath, result):
    with open(filepath, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            for _, _, json_object in jsonfinder(line, json_only=True):
                if isinstance(json_object, dict):
                    text = json_object.get("text")
                    if text:
                        if os.path.basename(filepath) not in result:
                            result[os.path.basename(filepath)] = [text]
                        else:
                            result[os.path.basename(filepath)].append(text)
                else:
                    pattern = r'"text":"(.*?)"'
                    matches = re.findall(pattern, line)
                    if matches:
                        for match in matches:
                            if os.path.basename(filepath) not in result:
                                result[os.path.basename(filepath)] = [match]
                            else:
                                result[os.path.basename(filepath)].append(match)


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mcfunction"):
            filepath = os.path.join(root, file)
            process_mcfunction_file(filepath, result)

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
