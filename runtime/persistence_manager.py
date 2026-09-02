# Source Generated with Decompyle++
# File: persistence_manager.cpython-312.pyc (Python 3.12)

import os
import json
from datetime import datetime
from typing import Dict, Any
from orchestrator.memory_manager import MemoryManager
from orchestrator.memory_vectorstore import VectorMemory

class PersistenceManager:

    def __init__(self = None, base_path = None):
        self.base_path = base_path
        self.logs_path = os.path.join(base_path, 'logs')
        self.workspace_path = os.path.join(base_path, 'project_workspace')
        self.memory_path = os.path.join(base_path, 'memory')
        self.vectorstore_path = os.path.join(base_path, 'vectorstore')
        os.makedirs(self.logs_path, exist_ok = True)
        os.makedirs(self.workspace_path, exist_ok = True)
        os.makedirs(self.memory_path, exist_ok = True)
        os.makedirs(self.vectorstore_path, exist_ok = True)
        self.memory = MemoryManager(self.memory_path)
        self.vector_memory = VectorMemory(self.vectorstore_path)


    def _timestamp(self):
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


    def save_log(self = None, log_type = None, data = None):
        timestamp = self._timestamp()
        filename = f'''{timestamp}_{log_type}.json'''
        path = os.path.join(self.logs_path, filename)
        f = open(path, 'w', encoding = 'utf-8')
        json.dump(data, f, indent = 2, ensure_ascii = False)
        None(None, None)
        return None
        with None:
            if not None:
                pass


    def save_workspace_file(self = None, relative_path = None, content = None):
        full_path = os.path.join(self.workspace_path, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok = True)
        f = open(full_path, 'w', encoding = 'utf-8')
        f.write(content)
        None(None, None)
        return None
        with None:
            if not None:
                pass


    def save_memory(self = None, agent = None, task_id = None, content = (None,), metadata = ('agent', str, 'task_id', str, 'content', Any, 'metadata', Dict[(str, Any)])):
        if not metadata:
            metadata
        entry = {
            'agent': agent,
            'task_id': task_id,
            'content': content,
            'metadata': { },
            'timestamp': self._timestamp() }
        self.memory.save(entry)
        self.vector_memory.add(entry)


    def save_execution(self, task = None, orchestrator_output = None, agent_output = None, qa_output = ('task', Dict[(str, Any)], 'orchestrator_output', str, 'agent_output', str, 'qa_output', str)):
        execution_data = {
            'timestamp': self._timestamp(),
            'task': task,
            'orchestrator_output': orchestrator_output,
            'agent_output': agent_output,
            'qa_output': qa_output }
        self.save_log('execution', execution_data)
        self.save_memory(agent = 'system', task_id = task.get('task_id', 'unknown'), content = execution_data, metadata = {
            'type': 'execution' })


    def save_generated_code(self = None, filename = None, code = None, agent = ('backend',)):
        self.save_workspace_file(filename, code)
        self.save_memory(agent = agent, task_id = 'generated_code', content = code, metadata = {
            'file': filename })


    def load_recent_logs(self = None, limit = None):
        files = sorted(os.listdir(self.logs_path), reverse = True)
        results = []
        for filename in files[:limit]:
            path = os.path.join(self.logs_path, filename)
            f = open(path, 'r', encoding = 'utf-8')
            results.append(json.load(f))
            None(None, None)
        return results
        with None:
            if not None:
                pass
        continue
        except Exception:
            continue
