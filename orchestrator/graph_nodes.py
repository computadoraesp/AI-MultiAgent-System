# Source Generated with Decompyle++
# File: graph_nodes.cpython-312.pyc (Python 3.12)

import os
import json
from typing import TypedDict, Dict, Any
from langchain_core.prompts import PromptTemplate
from orchestrator.task_schema import Task, TaskContext
from runtime.output_parser import parse_agent_output
from orchestrator.agent_router_semantic import get_router
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def _get_components():
    init_components = init_components
    import orchestrator.system_init
    return init_components()


def load_prompt(path = None):
    f = open(path, 'r', encoding = 'utf-8')
    None(None, None)
    return
    with None:
        if not None, f.read():
            pass

system_prompt = load_prompt(os.path.join(BASE_PATH, 'models', 'system_prompt.txt'))
orchestrator_prompt = load_prompt(os.path.join(BASE_PATH, 'orchestrator', 'prompt.txt'))
agent_prompts = {
    'architecture': load_prompt(os.path.join(BASE_PATH, 'agents', 'architecture', 'prompt.txt')),
    'backend': load_prompt(os.path.join(BASE_PATH, 'agents', 'backend', 'prompt.txt')),
    'frontend': load_prompt(os.path.join(BASE_PATH, 'agents', 'frontend', 'prompt.txt')),
    'ai_deeplearning': load_prompt(os.path.join(BASE_PATH, 'agents', 'ai_deeplearning', 'prompt.txt')),
    'devops': load_prompt(os.path.join(BASE_PATH, 'agents', 'devops', 'prompt.txt')),
    'qa': load_prompt(os.path.join(BASE_PATH, 'agents', 'qa', 'prompt.txt')) }

class OrchestratorState(TypedDict):
    retry_count: int = 'OrchestratorState'


def run_agent(agent_name = None, task_obj = None):
    prompt = f'''\n{system_prompt}\n\n{agent_prompts[agent_name]}\n\nTASK ID:\n{task_obj.task_id}\n\nOBJECTIVE:\n{task_obj.objective}\n\nCONTEXT:\n{json.dumps(task_obj.context.model_dump(), indent = 2, ensure_ascii = False)}\n\nEXPECTED OUTPUT:\n{task_obj.expected_output}\n\nOUTPUT FORMAT:\n{task_obj.output_format}\n\nPRIORITY:\n{task_obj.priority}\n'''
    components = _get_components()
    result = components['runtime'].invoke(agent_name = agent_name, prompt = prompt)
    return str(result)


def detect_agent(orchestrator_output = None):
    router = get_router()
    return router.route(orchestrator_output)


def orchestrator_step(state = None):
    task = state['task']
    objective = task['objective']
    assigned_agent = task.get('assigned_agent')
    components = _get_components()
    json_memory = components['memory'].search(objective, limit = 5)
    semantic_memory = components['vector_memory'].search(objective, k = 5)
    memory_context = {
        'json_memory': json_memory,
        'semantic_memory': semantic_memory }
    template = PromptTemplate(input_variables = [
        'task',
        'memory'], template = f'''\n{system_prompt}\n\nMEMORY CONTEXT:\n{{memory}}\n\n{orchestrator_prompt}\n\nUSER TASK:\n{{task}}\n''')
    prompt = template.format(task = objective, memory = json.dumps(memory_context, indent = 2, ensure_ascii = False))
    result = components['runtime'].invoke(agent_name = 'orchestrator', prompt = prompt)
    if assigned_agent:
        selected_agent = assigned_agent
    else:
        router = get_router()
        selected_agent = router.route(objective)
    return {
        'orchestrator_output': str(result),
        'selected_agent': selected_agent,
        'retry_count': 0 }


def agent_step(state = None):
    task = state['task']
    selected_agent = state['selected_agent']
    components = _get_components()
    context = TaskContext(requirements = [
        task['objective']], memory = components['memory'].search(task['objective'], limit = 3), metadata = {
        'semantic_memory': components['vector_memory'].search(task['objective'], k = 3),
        'orchestrator_output': state['orchestrator_output'] })
    task_obj = Task(agent = selected_agent, objective = task['objective'], context = context, expected_output = 'production-ready implementation', output_format = 'code')
    result = run_agent(selected_agent, task_obj)
    parsed_result = parse_agent_output(result)
    return {
        'agent_output': parsed_result }


def qa_step(state = None):
    prompt = f'''\n{system_prompt}\n\nYou are validating an AI-generated result.\n\nTASK:\n{state['task']['objective']}\n\nAGENT:\n{state['selected_agent']}\n\nOUTPUT:\n{state['agent_output']}\n\nVALIDATION RULES:\n- Check correctness\n- Check consistency\n- Check architecture alignment\n- Detect hallucinations\n- Detect fake APIs\n- Detect missing implementation\n\nReturn ONLY:\n\nAPPROVED\n\nor\n\nREJECTED: <short reason>\n'''
    components = _get_components()
    result = components['runtime'].invoke(agent_name = 'qa', prompt = prompt)
    return {
        'qa_output': str(result) }


def qa_router(state = None):
    qa_text = state['qa_output'].lower()
    retry_count = state.get('retry_count', 0)
    components = _get_components()
    max_retries = components['config'].get('execution_policy', { }).get('max_retries', 2)
    if 'approved' in qa_text:
        return 'save'
    if retry_count >= max_retries:
        return 'save'
    return 'retry'


def retry_step(state = None):
    retry_count = state.get('retry_count', 0) + 1
    prompt = f'''\nFix the following implementation.\n\nTASK:\n{state['task']['objective']}\n\nCURRENT OUTPUT:\n{state['agent_output']}\n\nQA FEEDBACK:\n{state['qa_output']}\n\nRULES:\n- Correct only the detected issues\n- Keep architecture consistency\n- Return complete corrected implementation\n'''
    components = _get_components()
    result = components['runtime'].invoke(agent_name = state['selected_agent'], prompt = prompt)
    parsed_result = parse_agent_output(str(result))
    return {
        'agent_output': parsed_result,
        'retry_count': retry_count }


def save_step(state = None):
    components = _get_components()
    components['persistence'].save_execution(task = state['task'], orchestrator_output = state['orchestrator_output'], agent_output = state['agent_output'], qa_output = state['qa_output'])
    components['persistence'].save_memory(agent = state['selected_agent'], task_id = state['task'].get('task_id', 'unknown'), content = state['agent_output'], metadata = {
        'qa_output': state['qa_output'] })

    try:
        project_name = state['task'].get('project_name')
        agent_output = state['agent_output']
        if isinstance(agent_output, dict):
            files = agent_output.get('files', [])
            if files:
                components['project_builder'].build(agent_output, project_name = project_name)
                return state
            text = None.get('summary', '')
            if text:
                components['project_builder'].build_from_text(text, state['selected_agent'], project_name = project_name)
        return state
    except Exception:
        e = None
        print('PROJECT BUILD SKIPPED:', str(e))
        e = None
        del e
        return state
        e = None
        del e
