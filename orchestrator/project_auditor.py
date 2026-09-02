# Source Generated with Decompyle++
# File: project_auditor.cpython-312.pyc (Python 3.12)

import json
from typing import Dict, List, Any

class ProjectAuditor:

    def __init__(self, runtime):
        self.runtime = runtime


    def analyze(self = None, project_data = None, instructions = None):
        prompt = self._build_prompt(project_data, instructions)
        result = self.runtime.invoke(agent_name = 'qa', prompt = prompt)
        return self._parse_suggestions(str(result))


    def _build_prompt(self = None, project_data = None, instructions = None):
        files_summary = []
        for f in project_data['files']:
            content_preview = ''
            if f.get('content'):
                lines = f['content'].split('\n')
                preview = lines[:30]
                content_preview = '\n'.join(preview)
                if len(lines) > 30:
                    content_preview += '\n... (truncated)'
            files_summary.append(f'''=== {f['path']} ({f['size']} bytes) ===\n{content_preview}''')
        joined_files = '\n\n'.join(files_summary)
        return f'''\nYou are a senior software engineer conducting a code review.\n\nAnalyze the project below and suggest concrete improvements.\n\nINSTRUCTIONS:\n{instructions if instructions else 'Identify bugs, code smells, missing error handling, security issues, and architecture improvements.'}\n\nPROJECT STRUCTURE:\n{json.dumps(project_data.get('structure', []), indent = 2)}\n\nFILES:\n{joined_files}\n\nFor each suggestion, return a JSON array with this exact format.\nReturn ONLY valid JSON, no other text:\n\n[\n  {{\n    "id": 1,\n    "priority": "critical" | "high" | "medium" | "low",\n    "file": "relative/path/to/file.py",\n    "description": "What the issue is and how to fix it",\n    "action": "modify" | "create" | "delete",\n    "new_content": "Complete new file content (if modify or create)",\n    "original_snippet": "Small snippet of original code being changed (if modify)"\n  }}\n]\n\nRULES:\n- Each suggestion MUST have a different id\n- For \'modify\' actions, include the full new file content in new_content\n- For \'create\' actions, set file to the new file path and include full content\n- For \'delete\' actions, new_content can be empty\n- Be specific and actionable\n- Maximum 10 suggestions\n'''


    def _parse_suggestions(self = None, raw = None):

        try:
            data = json.loads(raw)
            if not isinstance(data, list):
                data = []
            for item in data:
                item.setdefault('priority', 'medium')
                item.setdefault('action', 'modify')
                item.setdefault('new_content', '')
                item.setdefault('original_snippet', '')
            return data
        except json.JSONDecodeError:
            import re
            match = re.search('\\[.*\\]', raw, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                except (json.JSONDecodeError, ValueError):
                    data = []
                except:
                    data = []
