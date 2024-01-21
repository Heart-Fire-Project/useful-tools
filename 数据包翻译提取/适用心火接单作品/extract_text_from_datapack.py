# -*- coding: UTF-8 -*-
import os
import json
import re

from jsonfinder import jsonfinder

directory = "data/"
output_file = "data/text/text.json"
result_dict = {}


def process_json_object(json_obj, res_dict):
    if isinstance(json_obj, dict):
        text = json_obj.get("text")
        if text and text not in res_dict:
            res_dict[text] = text


def process_mcfunction_file(mcfunction_path, res_dict):
    relpath = os.path.relpath(mcfunction_path, directory)
    path_parts = relpath.split(os.sep)
    current_dict = res_dict

    for part in path_parts[:-1]:
        if part not in current_dict:
            current_dict[part] = {}
        current_dict = current_dict[part]

    with open(mcfunction_path, "r", encoding="UTF-8") as file_obj:
        lines = file_obj.readlines()
        for line in lines:
            for _, _, json_obj in jsonfinder(line, json_only=True):
                if isinstance(json_obj, dict):
                    text = json_obj.get("text")
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
            mcfunc_path = os.path.join(root, file)
            process_mcfunction_file(mcfunc_path, result_dict)

with open(output_file, "w", encoding="UTF-8") as output_file_obj:
    json.dump(result_dict, output_file_obj, ensure_ascii=False, indent=4)
