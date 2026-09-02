# Source Generated with Decompyle++
# File: task_graph.cpython-312.pyc (Python 3.12)

from typing import List, Dict, Set
from orchestrator.task_schema import Task

class TaskGraph:

    def __init__(self = None, tasks = None):
        self.tasks = tasks
        self.completed = set()
        self.running = set()
    # WARNING: Decompyle incomplete


    def _validate_graph(self):
        for task in self.tasks:
            for dependency in task.dependencies:
                if not dependency not in self.task_map:
                    continue
                raise ValueError(f'''Missing dependency: {dependency}''')
        self._detect_cycles()


    def _detect_cycles(self):
        pass
    # WARNING: Decompyle incomplete


    def is_complete(self = None):
        return len(self.completed) == len(self.tasks)


    def get_ready_tasks(self = None):
        pass
    # WARNING: Decompyle incomplete


    def mark_complete(self = None, task_id = None):
        self.completed.add(task_id)
        self.running.discard(task_id)


    def has_deadlock(self = None):
        if self.is_complete():
            return False
        ready_tasks = self.get_ready_tasks()
        return len(ready_tasks) == 0
