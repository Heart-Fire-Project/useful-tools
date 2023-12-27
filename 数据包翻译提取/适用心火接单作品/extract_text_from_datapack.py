# -*- coding: UTF-8 -*-
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
    relpath = os.path.relpath(filepath, directory)
    path_parts = relpath.split(os.sep)
    current_dict = result

    for part in path_parts[:-1]:
        if part not in current_dict:
            current_dict[part] = {}
        current_dict = current_dict[part]

    with open(filepath, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            for _, _, json_object in jsonfinder(line, json_only=True):
                if isinstance(json_object, dict):
                    text = json_object.get("text")
                    if text:
                        filename = path_parts[-1]
                        if filename not in current_dict:
                            current_dict[filename] = [text]
                        else:
                            current_dict[filename].append(text)
                else:
                    pattern = r'"text":"(.*?)"'
                    matches = re.findall(pattern, line)
                    if matches:
                        for match in matches:
                            filename = path_parts[-1]
                            if filename not in current_dict:
                                current_dict[filename] = [match]
                            else:
                                current_dict[filename].append(match)


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mcfunction"):
            filepath = os.path.join(root, file)
            process_mcfunction_file(filepath, result)

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
