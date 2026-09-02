# Source Generated with Decompyle++
# File: ollama_manager.cpython-312.pyc (Python 3.12)

import json
import requests
from typing import Dict, Any
from langchain_ollama import OllamaLLM

class OllamaManager:

    def __init__(self = None, config = None):
        self.config = config
        self.primary_model = config['primary_model']
        self.fallback_model = config['fallback_model']
        self.agent_models = config.get('agent_models', { })
        self.params = config.get('params', { })
        self.context_limits = config.get('context_limits', { })
        self.execution_policy = config.get('execution_policy', { })
        self.ollama_host = 'http://localhost:11434'


    def health_check(self = None):

        try:
            response = requests.get(f'''{self.ollama_host}/api/tags''', timeout = 5)
            return response.status_code == 200
        except Exception:
            return False



    def get_agent_model(self = None, agent_name = None):
        return self.agent_models.get(agent_name, self.primary_model)


    def get_context_limit(self = None, agent_name = None):
        return self.context_limits.get(agent_name, self.params.get('num_ctx', 4096))


    def create_llm(self = None, agent_name = None):
        model_name = self.get_agent_model(agent_name)
        context_limit = self.get_context_limit(agent_name)

        try:
            llm = OllamaLLM(model = model_name, num_ctx = context_limit, temperature = self.params.get('temperature', 0.2), top_p = self.params.get('top_p', 0.9), repeat_penalty = self.params.get('repeat_penalty', 1.1))
            return llm
        except Exception:
            return



    def _fallback_llm(self):
        return OllamaLLM(model = self.fallback_model, num_ctx = 4096, temperature = 0.1)


    def invoke(self = None, agent_name = None, prompt = None):
        if not self.health_check():
            raise RuntimeError('Ollama server is not running.')
        max_retries = self.execution_policy.get('max_retries', 2)
        attempt = 0
        last_error = None
        if attempt <= max_retries:

            try:
                llm = self.create_llm(agent_name)
                response = llm.invoke(prompt)
                if not response:
                    raise RuntimeError('Empty LLM response.')
                return response
                raise RuntimeError(f'''LLM execution failed: {last_error}''')
            except Exception:
                e = None
                last_error = e
                attempt += 1
                e = None
                del e
            except:
                e = None
                del e

            if attempt <= max_retries:
                continue
        continue



def load_model_config(path = None):
    f = open(path, 'r', encoding = 'utf-8')
    None(None, None)
    return
    with None:
        if not None, json.load(f):
            pass
