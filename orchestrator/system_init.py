# Source Generated with Decompyle++
# File: system_init.cpython-312.pyc (Python 3.12)

import os
from runtime.ollama_manager import OllamaManager, load_model_config
from runtime.persistence_manager import PersistenceManager
from runtime.workspace_manager import WorkspaceManager
from runtime.project_builder import ProjectBuilder
from orchestrator.memory_manager import MemoryManager
from orchestrator.memory_vectorstore import VectorMemory
from planner.planner import PlannerAgent
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VECTORSTORE_PATH = os.path.join(BASE_PATH, 'vectorstore')
MEMORY_PATH = os.path.join(BASE_PATH, 'memory')
OUTPUT_PROJECTS_PATH = os.path.join(BASE_PATH, 'output', 'projects')
CONFIG_PATH = os.path.join(BASE_PATH, 'models', 'model_config.json')
_shared_components = None

def init_components():
    '''
    Initialize all orchestrator-related components and
    return them in a structured dict. Uses a singleton cache
    to avoid multiple instances (e.g. redundant embedding loading).
    '''
    pass
# WARNING: Decompyle incomplete
