# Source Generated with Decompyle++
# File: output_parser.cpython-312.pyc (Python 3.12)

import json
import re
from typing import Dict, Any

def default_output():
    return {
        'summary': '',
        'files': [],
        'commands': [],
        'notes': [],
        'dependencies': [] }


def clean_output(text = None):
    if not text:
        return ''
    text = text.strip()
    text = text.replace('\r\n', '\n')
    return text


def extract_json_block(text = None):
    pattern = '\\{.*\\}'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return None
    return match.group(0)


def extract_code_blocks(text = None):
    pattern = '```(?:\\w+)?\\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def build_fallback_file(text = None):
    code_blocks = extract_code_blocks(text)
    if code_blocks:
        return [
            {
                'path': 'generated/output.py',
                'content': '\n\n'.join(code_blocks) }]


def validate_output_structure(data = None):
    result = default_output()
    result['summary'] = data.get('summary', '')
    result['files'] = data.get('files', [])
    result['commands'] = data.get('commands', [])
    result['notes'] = data.get('notes', [])
    result['dependencies'] = data.get('dependencies', [])
    return result


def parse_agent_output(text = None):
