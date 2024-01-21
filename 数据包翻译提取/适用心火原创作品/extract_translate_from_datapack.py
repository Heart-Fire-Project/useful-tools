# -*- coding: UTF-8 -*-
import os
import json
import re

from jsonfinder import jsonfinder

directory = "data/"
output_file = "data/lang/zh_cn.json"
result = {}


def extract_trans_fallb_old_version(json_obj, res_dict):
    if isinstance(json_obj, dict):
        translate = json_obj.get("translate")
        fallback = json_obj.get("fallback")
        if translate and fallback and translate not in res_dict:
            res_dict[translate] = fallback
        for value in json_obj.values():
            if isinstance(value, (dict, list)):
                extract_trans_fallb_old_version(value, res_dict)
    elif isinstance(json_obj, list):
        for item in json_obj:
            if isinstance(item, (dict, list)):
                extract_trans_fallb_old_version(item, res_dict)
    elif isinstance(json_obj, str):
        trans_fallb_dict = extract_trans_fallb_new_version(json_obj)
        res_dict.update(trans_fallb_dict)


def extract_trans_fallb_new_version(lin):
    matches = re.findall(r'(trans_\d+|fallb_\d+):"(.*?)"', lin)
    temp_dict = {}
    for match in matches:
        key, value = match
        key_type, key_num = key.split('_')
        if key_type == 'trans':
            if 'fallb_' + key_num in temp_dict:
                result[value] = temp_dict['fallb_' + key_num]
            else:
                temp_dict[key] = value
        elif key_type == 'fallb':
            if 'trans_' + key_num in temp_dict:
                result[temp_dict['trans_' + key_num]] = value
            else:
                temp_dict[key] = value
    return result


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mcfunction"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="UTF-8") as f:
                lines = f.readlines()
                for line in lines:
                    for _, _, json_object in jsonfinder(line, json_only=True):
                        extract_trans_fallb_old_version(json_object, result)

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
