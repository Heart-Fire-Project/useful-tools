# -*- coding: UTF-8 -*-
import os
import json
from jsonfinder import jsonfinder

directory = "data/"
output_file = "data/lang/zh_cn.json"
result = {}


def process_json_object(json_object, result):
    if isinstance(json_object, dict):
        translate = json_object.get("translate")
        fallback = json_object.get("fallback")
        if translate and fallback and translate not in result:
            result[translate] = fallback
        for value in json_object.values():
            if isinstance(value, (dict, list)):
                process_json_object(value, result)
    elif isinstance(json_object, list):
        for item in json_object:
            if isinstance(item, (dict, list)):
                process_json_object(item, result)


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mcfunction"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="UTF-8") as f:
                lines = f.readlines()
                for line in lines:
                    for _, _, json_object in jsonfinder(line, json_only=True):
                        process_json_object(json_object, result)

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
