import os
import json
from typing import List
from lcabyg_web_api_py.type_hinting import JsonList
from sbi_web_api_py.utils import pack_bytes


def collect_json(json_paths: List[str]) -> JsonList:
    assert isinstance(json_paths, list)
    out = list()
    for start_path in json_paths:
        start_path = os.path.expanduser(start_path)
        if os.path.isdir(start_path):
            for root, directories, files in os.walk(start_path):
                for file in files:
                    target_path = os.path.join(root, file)
                    if os.path.isfile(target_path) and os.path.splitext(target_path)[1].lower() == '.json':
                        with open(target_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        assert isinstance(data, list)
                        out.extend(data)
        else:
            with open(start_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert isinstance(data, list)
            out.extend(data)

    return out


def pack_json(data: JsonList):
    text = json.dumps(data, ensure_ascii=False)
    encoded_text = pack_bytes(text.encode('utf-8'))
    return encoded_text
