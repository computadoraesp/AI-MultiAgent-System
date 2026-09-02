# Source Generated with Decompyle++
# File: json_parser.cpython-312.pyc (Python 3.12)

import json
import re
from typing import Any

def extract_json(text = None):

    try:
        return json.loads(text)
    except Exception:
        pass

    cleaned = re.sub('```json|```', '', text, flags = re.IGNORECASE).strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    array_pattern = '\\[.*\\]'
    array_match = re.search(array_pattern, cleaned, re.DOTALL)
    if array_match:
        json_text = array_match.group(0)

        try:
            return json.loads(json_text)
        except Exception:
            pass

        object_pattern = '\\{.*\\}'
        object_match = re.search(object_pattern, cleaned, re.DOTALL)
        if object_match:
            json_text = object_match.group(0)

            try:
                return json.loads(json_text)
            except Exception:
                e = None
                raise ValueError(f'''Invalid JSON object: {str(e)}''')
                e = None
                del e
                raise ValueError('No valid JSON found.')
