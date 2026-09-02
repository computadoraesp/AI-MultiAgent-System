# Source Generated with Decompyle++
# File: task_executor.cpython-312.pyc (Python 3.12)

from orchestrator.task_schema import Task
from orchestrator.graph_builder import build_agent_graph
graph = build_agent_graph()

def execute_planned_task(planned_task = None):
    result = graph.invoke({
        'task': {
            'task_id': planned_task.task_id,
            'objective': planned_task.objective,
            'dependencies': planned_task.dependencies,
            'priority': planned_task.priority,
            'assigned_agent': planned_task.agent } })
    return result.get('agent_output', 'No output generated.')
