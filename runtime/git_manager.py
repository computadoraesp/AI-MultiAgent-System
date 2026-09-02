# Source Generated with Decompyle++
# File: git_manager.cpython-312.pyc (Python 3.12)

import os
import re
import subprocess
import json
from typing import Optional, Tuple
GITHUB_PATTERN = re.compile('https?://github\\.com/([^/\\s]+/[^/\\s.#?]+)')
PUSH_KEYWORDS = [
    'push',
    'sub',
    'upload',
    'public',
    'crea repositorio',
    'create repo',
    'nuevo repo',
    'nuevo repositorio']
CLONE_KEYWORDS = [
    'clone',
    'clona',
    'descarga',
    'download',
    'trae']

class GitManager:

    def parse_github_url(self = None, text = None):
        match = GITHUB_PATTERN.search(text)
        if match:
            return match.group(0).rstrip('/').rstrip('.git')


    def extract_repo_name(self = None, text = None):
        url = self.parse_github_url(text)
        if url:
            return url.rstrip('/').split('/')[-1]
        match = None.search('(?:repositorio|repo|repository)\\s+["\\\']?(\\w[\\w.-]+)["\\\']?', text, re.I)
        if match:
            return match.group(1)


    def has_github_action(self = None, text = None):
        lower = text.lower()
        for kw in PUSH_KEYWORDS:
            if not kw in lower:
                continue
            PUSH_KEYWORDS
            return 'push'
        for kw in CLONE_KEYWORDS:
            if not kw in lower:
                continue
            CLONE_KEYWORDS
            return 'clone'
        if 'github.com' in lower:
            return 'clone'


    def clone_repo(self = None, url = None, target_path = None, token = (None,)):
        if token:
            url = url.replace('https://', f'''https://{token}@''')
        result = subprocess.run([
            'git',
            'clone',
            url,
            target_path], capture_output = True, text = True, timeout = 120)
        if result.returncode != 0:
            raise RuntimeError(f'''Git clone failed: {result.stderr.strip()}''')
        return result.stdout.strip()


    def init_repo(self = None, path = None):
        subprocess.run([
            'git',
            'init'], cwd = path, capture_output = True, text = True, timeout = 30)
        return self._git([
            'checkout',
            '-b',
            'main'], path)


    def create_gitignore(self = None, path = None):
        content = '# Python\n__pycache__/\n*.py[cod]\n*.egg-info/\n.venv/\nenv/\nvenv/\n\n# IDE\n.vscode/\n.idea/\n*.swp\n*.swo\n\n# OS\n.DS_Store\nThumbs.db\n\n# Project\n.env\n*.log\nnode_modules/\ndist/\nbuild/\n'
        filepath = os.path.join(path, '.gitignore')
        f = open(filepath, 'w', encoding = 'utf-8')
        f.write(content)
        None(None, None)
        return filepath
        with None:
            if not None:
                pass
        return filepath


    def commit_all(self = None, path = None, message = None):
        self._git([
            'add',
            '-A'], path)
        return self._git([
            'commit',
            '-m',
            message], path)


    def create_github_repo(self = None, token = None, repo_name = None, private = (True,)):
        import urllib.request as urllib
        import urllib.error as urllib
        visibility = 'private' if private else 'public'
        data = json.dumps({
            'name': repo_name,
            'private': private,
            'auto_init': False }).encode('utf-8')
        req = urllib.request.Request('https://api.github.com/user/repos', data = data, headers = {
            'Authorization': f'''token {token}''',
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3+json' })

        try:
            resp = urllib.request.urlopen(req, timeout = 30)
            body = json.loads(resp.read().decode('utf-8'))
            return body.get('clone_url', f'''https://github.com/{body['full_name']}.git''')
        except urllib.error.HTTPError:
            e = None
            body = e.read().decode('utf-8')
            raise RuntimeError(f'''GitHub API error ({e.code}): {body}''')
            e = None
            del e



    def push_to_github(self = None, path = None, token = None, repo_url = ('path', str, 'token', str, 'repo_url', str, 'return', str)):
        authed_url = repo_url.replace('https://', f'''https://{token}@''')
        self._git([
            'remote',
            'add',
            'origin',
            authed_url], path)
        return self._git([
            'push',
            '-u',
            'origin',
            'main'], path)


    def _git(self = None, args = None, path = None):
        result = subprocess.run([
            'git'] + args, cwd = path, capture_output = True, text = True, timeout = 60)
        if result.returncode != 0:
            raise RuntimeError(f'''git {' '.join(args)} failed: {result.stderr.strip()}''')
        return result.stdout.strip()


    def handle_construct_push(self = None, project_path = None, repo_name = None, token = (True,), private = ('project_path', str, 'repo_name', str, 'token', str, 'private', bool, 'return', str)):
        lines = []
        self.init_repo(project_path)
        lines.append('✓ git init')
        self.create_gitignore(project_path)
        lines.append('✓ .gitignore created')
        self.commit_all(project_path, 'Initial commit by AI Multi-Agent System')
        lines.append('✓ git commit')
        repo_url = self.create_github_repo(token, repo_name, private)
        lines.append(f'''✓ GitHub repo created: {repo_url}''')
        self.push_to_github(project_path, token, repo_url)
        lines.append(f'''✓ Pushed to {repo_url}''')
        return '\n'.join(lines)


    def handle_clone_review(self = None, url = None, target_path = None, token = (None,)):
        self.clone_repo(url, target_path, token)
        return f'''✓ Cloned {url} to {target_path}'''



def get_git_manager():
    return GitManager()
