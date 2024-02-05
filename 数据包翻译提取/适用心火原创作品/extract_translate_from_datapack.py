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


def extract_trans_fallb_new_version(line):
    matches = re.findall(r'(trans_\d+|fallb_\d+):"(.*?)"', line)
    result = {}
    for match in matches:
        key, value = match
        key_type, key_num = key.split('_')
        if key_type == 'trans':
            if 'fallb_' + key_num in result:
                result[result['fallb_' + key_num]] = value
                del result['fallb_' + key_num]
            else:
                result[key] = value
        elif key_type == 'fallb':
            if 'trans_' + key_num in result:
                result[value] = result['trans_' + key_num]
                del result['trans_' + key_num]
            else:
                result[key] = value
    result = {v: k for k, v in result.items()}
    return result


def extract_trans_fallb_json(json_obj):
    tag_str = json_obj.get('tag')
    if tag_str:
        translate_match = re.search(r'"translate":"(.*?)"', tag_str)
        fallback_match = re.search(r'"fallback":"(.*?)"', tag_str)
        if translate_match and fallback_match:
            translate = translate_match.group(1)
            fallback = fallback_match.group(1)
            return {translate: fallback}
    return {}


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".mcfunction"):
            filepath = os.path.join(root, file)
            print("正在处理" + filepath)
            with open(filepath, "r", encoding="UTF-8") as f:
                lines = f.readlines()
                for line in lines:
                    new_version_dict = extract_trans_fallb_new_version(line)
                    if new_version_dict:
                        result.update(new_version_dict)
                    else:
                        for _, _, json_object in jsonfinder(line, json_only=True):
                            extract_trans_fallb_old_version(json_object, result)
        if file.endswith("json"):
            filepath = os.path.join(root, file)
            print("正在处理" + filepath)
            with open(filepath, "r", encoding="UTF-8") as f:
                json_obj = json.load(f)
                result.update(extract_trans_fallb_json(json_obj))

with open(output_file, "w", encoding="UTF-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
