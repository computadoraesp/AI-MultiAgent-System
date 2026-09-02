# Source Generated with Decompyle++
# File: project_reader.cpython-312.pyc (Python 3.12)

import os
import json
from typing import Dict, List, Any
IGNORED_DIRS = {
    '.git',
    '.idea',
    '.venv',
    '.vscode',
    'logs',
    'venv',
    'memory',
    'output',
    '__pycache__',
    'vectorstore',
    'node_modules'}
IGNORED_EXT = {
    '.a',
    '.o',
    '.7z',
    '.gz',
    '.so',
    '.avi',
    '.bin',
    '.bmp',
    '.dll',
    '.doc',
    '.exe',
    '.gif',
    '.ico',
    '.jpg',
    '.lib',
    '.mov',
    '.mp3',
    '.mp4',
    '.obj',
    '.otf',
    '.pdf',
    '.png',
    '.pyc',
    '.pyd',
    '.pyo',
    '.rar',
    '.tar',
    '.ttf',
    '.wav',
    '.xls',
    '.zip',
    '.docx',
    '.jpeg',
    '.woff',
    '.xlsx',
    '.dylib',
    '.woff2'}

class ProjectReader:

    def __init__(self = None, max_files = None, max_size_kb = None):
        self.max_files = max_files
        self.max_size_kb = max_size_kb


    def read(self = None, project_path = None):
        if not os.path.isdir(project_path):
            raise NotADirectoryError(f'''Project path does not exist: {project_path}''')
        files = []
        total_size = 0
    # WARNING: Decompyle incomplete


    def _build_tree(self = None, root = None):
        tree = []
        for name in sorted(os.listdir(root)):
            if name in IGNORED_DIRS:
                continue
            path = os.path.join(root, name)
            if os.path.isdir(path):
                children = self._build_tree(path)
                tree.append({
                    'type': 'directory',
                    'name': name,
                    'children': children })
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in IGNORED_EXT:
                continue
            tree.append({
                'type': 'file',
                'name': name })
        return tree


    def summary(self = None, project_path = None):
        data = self.read(project_path)
        lines = [
            f'''Project: {data['project_path']}''']
        lines.append(f'''Files: {data['total_files']}''')
        lines.append(f'''Total size: {data['total_size_kb']} KB''')
        extensions = { }
        for f in data['files']:
            ext = os.path.splitext(f['path'])[1]
            extensions[ext] = extensions.get(ext, 0) + 1
        if extensions:
            lines.append('Languages:')
            for ext, count in sorted(extensions.items(), key = (lambda x: -x[1])):
                lines.append(f'''  {ext}: {count} files''')
        return '\n'.join(lines)
