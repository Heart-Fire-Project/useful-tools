# -*- coding: UTF-8 -*-
import os
import json
import re

directory = "data/"
insert_file = "data/text/text.json"


def insert_text_into_file(json_object, directory):
    for key, value in json_object.items():
        if isinstance(value, dict):
            insert_text_into_file(value, os.path.join(directory, key))
        elif isinstance(value, list):
            filepath = os.path.join(directory, key)
            with open(filepath, "r+", encoding="UTF-8") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    for item in value:
                        pattern = r'(\{"text":")(.*?)(",)'
                        replacement = r"\1" + item + r"\3"
                        lines[i] = re.sub(pattern, replacement, line)
                f.seek(0)
                f.writelines(lines)
                f.truncate()
        else:
            pass


with open(insert_file, "r", encoding="UTF-8") as f:
    data = json.load(f)

insert_text_into_file(data, directory)
