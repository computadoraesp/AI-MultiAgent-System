# Source Generated with Decompyle++
# File: project_builder.cpython-312.pyc (Python 3.12)

import re
import os
import json
from datetime import datetime
from typing import Dict, Any, List
from runtime.output_parser import clean_output, extract_code_blocks, extract_json_block
AGENT_FOLDER_MAP = {
    'architecture': 'docs',
    'backend': 'backend',
    'frontend': 'frontend',
    'ai_deeplearning': 'ai',
    'devops': 'deploy',
    'qa': 'tests' }
EXTENSION_FOLDER_MAP = {
    '.py': 'scripts',
    '.js': 'frontend',
    '.jsx': 'frontend',
    '.ts': 'frontend',
    '.tsx': 'frontend',
    '.html': 'frontend',
    '.css': 'frontend',
    '.json': 'config',
    '.yaml': 'deploy',
    '.yml': 'deploy',
    '.sh': 'deploy',
    '.dockerfile': 'deploy',
    '.md': 'docs',
    '.txt': 'docs' }

def contains_json(text = None):
    if '{' in text:
        '{' in text
    return '}' in text


def contains_markdown(text = None):
    pass
# WARNING: Decompyle incomplete


def detect_file_structure(text = None):
    pass
# WARNING: Decompyle incomplete


def extract_final_answer(text = None):
    text = clean_output(text)
    code_blocks = extract_code_blocks(text)
    if code_blocks:
        return '\n\n'.join(code_blocks)


def parse_agent_output(text = None):
    cleaned = clean_output(text)
    code_blocks = extract_code_blocks(cleaned)
    json_payload = extract_json_block(cleaned)
    final_answer = extract_final_answer(cleaned)
    return {
        'raw': cleaned,
        'final_output': final_answer,
        'contains_code': len(code_blocks) > 0,
        'contains_json': json_payload is not None,
        'contains_markdown': contains_markdown(cleaned),
        'contains_project_structure': detect_file_structure(cleaned),
        'code_blocks': code_blocks,
        'json_payload': json_payload,
        'code_block_count': len(code_blocks),
        'output_length': len(cleaned) }


class ProjectBuilder:

    def __init__(self, workspace_manager):
        self.workspace = workspace_manager


    def build(self = None, payload = None, project_name = None):
        saved_paths = []
        if isinstance(payload, dict):
            files = payload.get('files', [])
            for file_entry in files:
                if not isinstance(file_entry, dict):
                    continue
                path = file_entry.get('path')
                content = file_entry.get('content', '')
                if not path:
                    continue
                if not content:
                    continue
                full_path = self.workspace.save_file(path, content)
                saved_paths.append(full_path)
            return saved_paths
        if None(payload, str):
            code_blocks = extract_code_blocks(payload)
            for index, block in enumerate(code_blocks):
                ext = self._detect_extension(block)
                folder = EXTENSION_FOLDER_MAP.get(ext, 'misc')
                filename = f'''{folder}/output_{index}{ext}'''
                full_path = self.workspace.save_file(filename, block)
                saved_paths.append(full_path)
        return saved_paths


    def build_from_text(self = None, text = None, agent = None, project_name = ('unknown', None)):
        parsed = parse_agent_output(text)
        saved_paths = []
        folder = AGENT_FOLDER_MAP.get(agent, 'misc')
        for index, block in enumerate(parsed.get('code_blocks', [])):
            ext = self._detect_extension(block)
            filename = f'''{folder}/output_{index}{ext}'''
            full_path = self.workspace.save_file(filename, block)
            saved_paths.append(full_path)
        return saved_paths


    def save_project_info(self = None, project_name = None, metadata = None):
        info = {
            'project': project_name,
            'created': datetime.now().isoformat(),
            'agents': metadata.get('agents', []),
            'task': metadata.get('task', ''),
            'files_generated': metadata.get('files', 0),
            'status': metadata.get('status', 'unknown') }
        full_path = self.workspace.save_file('project_info.json', json.dumps(info, indent = 2, ensure_ascii = False))
        return full_path


    def _detect_extension(self = None, code_block = None):
        lines = code_block.strip().split('\n')
        first_line = lines[0].strip() if lines else ''
    # WARNING: Decompyle incomplete
