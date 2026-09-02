# Source Generated with Decompyle++
# File: agent_memory.cpython-312.pyc (Python 3.12)

import json
import os
from datetime import datetime

class AgentMemory:

    def __init__(self = None, path = None, agent_name = None):
        self.path = path
        self.agent_name = agent_name
        self.file = os.path.join(path, f'''{agent_name}_memory.json''')
        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            json.dump([], f)
            None(None, None)
            return None
        return None
        with None:
            if not None:
                pass


    def save(self, entry):
        data = self.load()
        entry['timestamp'] = datetime.utcnow().isoformat()
        data.append(entry)
        f = open(self.file, 'w')
        json.dump(data, f, indent = 2)
        None(None, None)
        return None
        with None:
            if not None:
                pass


    def load(self):
        f = open(self.file, 'r')
        None(None, None)
        return
        with None:
            if not None, json.load(f):
                pass
