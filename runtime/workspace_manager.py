# Source Generated with Decompyle++
# File: workspace_manager.cpython-312.pyc (Python 3.12)

import os
from typing import Dict, List

class WorkspaceManager:

    def __init__(self = None, base_path = None):
        self.base_path = base_path
        self._project_name = None
        self._project_path = None
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            return None


    def set_project(self = None, project_name = None):
        self._project_name = project_name
        self._project_path = os.path.join(self.base_path, project_name)
        os.makedirs(self._project_path, exist_ok = True)
        return self._project_path


    def project_path(self = None):
        if not self._project_path:
            self._project_path
        return self.base_path


    def save_file(self = None, relative_path = None, content = None):
        if self._project_path:
            full_path = os.path.join(self._project_path, relative_path)
        else:
            full_path = os.path.join(self.base_path, relative_path)
        folder = os.path.dirname(full_path)
        os.makedirs(folder, exist_ok = True)
        f = open(full_path, 'w', encoding = 'utf-8')
        f.write(content)
        None(None, None)
        return full_path
        with None:
            if not None:
                pass
        return full_path


    def save_code_blocks(self = None, blocks = None):
        saved_files = []
        for index, block in enumerate(blocks):
            language = block.get('language', 'txt')
            extension_map = {
                'python': '.py',
                'javascript': '.js',
                'typescript': '.ts',
                'json': '.json',
                'html': '.html',
                'css': '.css',
                'bash': '.sh' }
            extension = extension_map.get(language, '.txt')
            filename = f'''generated_{index}{extension}'''
            path = self.save_file(filename, block['code'])
            saved_files.append(path)
        return saved_files
