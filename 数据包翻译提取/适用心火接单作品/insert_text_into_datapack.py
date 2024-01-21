# -*- coding: UTF-8 -*-
import os
import json
import re

data_directory = "data/"
insert_file = "data/text/text.json"


def insert_text_into_file(json_object, dir_path):
    for key, value in json_object.items():
        if isinstance(value, dict):
            insert_text_into_file(value, os.path.join(dir_path, key))
        elif isinstance(value, list):
            filepath = os.path.join(dir_path, key)
            with open(filepath, "r+", encoding="UTF-8") as file_object:
                lines = file_object.readlines()
                for i, line in enumerate(lines):
                    for item in value:
                        pattern = r'(\{"text":")(.*?)(",)'
                        replacement = r"\1" + item + r"\3"
                        lines[i] = re.sub(pattern, replacement, line)
                file_object.seek(0)
                file_object.writelines(lines)
                file_object.truncate()
        else:
            pass


with open(insert_file, "r", encoding="UTF-8") as file_obj:
    data = json.load(file_obj)

insert_text_into_file(data, data_directory)
