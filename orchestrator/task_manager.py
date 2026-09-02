# Source Generated with Decompyle++
# File: task_manager.cpython-312.pyc (Python 3.12)

from orchestrator.task_schema import Task
import uuid

class TaskManager:

    def create_task(self, agent, objective, context, expected_output, output_format, priority = ('medium',)):
        return Task(task_id = str(uuid.uuid4()), agent = agent, objective = objective, context = context, expected_output = expected_output, output_format = output_format, priority = priority)


    def batch_tasks(self, tasks):
        pass
    # WARNING: Decompyle incomplete
