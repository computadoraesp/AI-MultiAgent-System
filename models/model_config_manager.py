# Source Generated with Decompyle++
# File: model_config_manager.cpython-312.pyc (Python 3.12)

import os
import sys
import json
import shutil
import subprocess
from typing import Dict, Any, Optional
from copy import deepcopy
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(BASE_PATH, 'models', 'model_config.json')
PRESETS_PATH = os.path.join(BASE_PATH, 'models', 'presets')

def load_config():
    f = open(CONFIG_PATH, 'r', encoding = 'utf-8')
    None(None, None)
    return
    with None:
        if not None, json.load(f):
            pass


def save_config(config = None):
    f = open(CONFIG_PATH, 'w', encoding = 'utf-8')
    json.dump(config, f, indent = 2, ensure_ascii = False)
    None(None, None)
    return None
    with None:
        if not None:
            pass


def get_ollama_models():

    try:
        result = subprocess.run([
            'ollama',
            'list'], capture_output = True, text = True, timeout = 10)
        lines = result.stdout.strip().split('\n')
        models = []
        for line in lines[1:]:
            parts = line.split()
            if not parts:
                continue

                try:
                    models.append(parts[0].replace(':latest', ''))
                    continue
                    return models
                except Exception:
                    return




def list_config():
    config = load_config()
    print('\n=== CONFIGURACIÓN ACTUAL ===\n')
    print(f'''  Modelo primario:     {config['primary_model']}''')
    print(f'''  Modelo coder:        {config['coder_model']}''')
    print(f'''  Modelo fallback:     {config['fallback_model']}''')
    print(f'''  Modelo embeddings:   {config['embedding_model']}''')
    print()
    print('  Agentes:')
    for agent, model in config.get('agent_models', { }).items():
        print(f'''    {agent:15s} -> {model}''')
    print()
    print('  Parámetros:')
    for k, v in config.get('params', { }).items():
        print(f'''    {k:20s} = {v}''')
    print()


def set_agent_model(agent = None, model_name = None):
    config = load_config()
    if agent not in config.get('agent_models', { }):
        print(f'''ERROR: Agente \'{agent}\' no válido.''')
        print(f'''  Agentes disponibles: {', '.join(config['agent_models'].keys())}''')
        return None
    config['agent_models'][agent] = model_name
    save_config(config)
    print(f'''OK: Agente \'{agent}\' ahora usa \'{model_name}\'''')


def set_primary(model_name = None):
    config = load_config()
    config['primary_model'] = model_name
    save_config(config)
    print(f'''OK: Modelo primario cambiado a \'{model_name}\'''')


def set_coder(model_name = None):
    config = load_config()
    config['coder_model'] = model_name
    save_config(config)
    print(f'''OK: Modelo coder cambiado a \'{model_name}\'''')


def set_embedding(model_name = None):
    config = load_config()
    config['embedding_model'] = model_name
    save_config(config)
    print(f'''OK: Modelo embeddings cambiado a \'{model_name}\'''')


def set_param(param = None, value = None):
    config = load_config()
    valid_params = [
        'num_ctx',
        'temperature',
        'top_p',
        'repeat_penalty']
    if param not in valid_params:
        print(f'''ERROR: Parámetro \'{param}\' no válido.''')
        print(f'''  Válidos: {', '.join(valid_params)}''')
        return None

    try:
        if param == 'num_ctx':
            config['params'][param] = int(value)
        else:
            config['params'][param] = float(value)
        save_config(config)
        print(f'''OK: {param} = {value}''')
        return None
    except ValueError:
        print(f'''ERROR: \'{value}\' no es un valor numérico válido''')
        return None



def apply_preset(name = None):
    preset_path = os.path.join(PRESETS_PATH, f'''{name}.json''')
    if not os.path.exists(preset_path):
        print(f'''ERROR: Preset \'{name}\' no encontrado.''')
        print(f'''  Presets disponibles: {list_available_presets()}''')
        return None
    f = open(preset_path, 'r', encoding = 'utf-8')
    preset = json.load(f)
    None(None, None)
# WARNING: Decompyle incomplete


def list_available_presets():
    if not os.path.exists(PRESETS_PATH):
        return '(ninguno)'
# WARNING: Decompyle incomplete


def save_preset(name = None):
    config = load_config()
    preset_path = os.path.join(PRESETS_PATH, f'''{name}.json''')
    f = open(preset_path, 'w', encoding = 'utf-8')
    json.dump(config, f, indent = 2, ensure_ascii = False)
    None(None, None)
    print(f'''OK: Configuración actual guardada como preset \'{name}\'''')
    return None
    with None:
        if not None:
            pass
    continue


def reset_defaults():
    config = load_config()
    default_models = {
        'agent_models': {
            'orchestrator': 'llama3.1:8b',
            'architecture': 'llama3.1:8b',
            'backend': 'deepseek-coder:6.7b-instruct-q4_K_M',
            'frontend': 'deepseek-coder:6.7b-instruct-q4_K_M',
            'qa': 'llama3.1:8b',
            'ai_deeplearning': 'deepseek-coder:6.7b-instruct-q4_K_M',
            'devops': 'deepseek-coder:6.7b-instruct-q4_K_M' },
        'params': {
            'num_ctx': 6144,
            'temperature': 0.1,
            'top_p': 0.9,
            'repeat_penalty': 1.1 } }
    for key, value in default_models.items():
        config[key] = value
    save_config(config)
    print('OK: Configuración restaurada a valores por defecto')


def interactive():
    config = load_config()
    local_models = get_ollama_models()
    print('\n============================================')
    print('  MODEL CONFIG MANAGER — Modo interactivo')
    print('============================================')
    print()
    print(f'''Configuración actual: {CONFIG_PATH}''')
    print()
    if local_models:
        print('Modelos disponibles en Ollama:')
        for m in local_models:
            print(f'''  - {m}''')
    else:
        print('(No se pudo obtener lista de modelos de Ollama)')
    print()
    print('\n--- MENÚ ---')
    print('1. Ver configuración actual')
    print('2. Cambiar modelo de un agente')
    print('3. Cambiar modelo primario')
    print('4. Cambiar modelo coder')
    print('5. Cambiar modelo embeddings')
    print('6. Cambiar parámetros (temperature, num_ctx...)')
    print('7. Aplicar preset de hardware')
    print('8. Guardar config actual como preset')
    print('9. Restaurar valores por defecto')
    print('0. Salir')
    print()
    choice = input('Selecciona una opción: ').strip()
    if choice == '1':
        list_config()
    elif choice == '2':
        agents = list(config.get('agent_models', { }).keys())
        print(f'''Agentes: {', '.join(agents)}''')
        agent = input('Nombre del agente: ').strip()
        model = input(f'''Modelo para \'{agent}\': ''').strip()
        if agent and model:
            set_agent_model(agent, model)
            config = load_config()
        elif choice == '3':
            model = input('Nuevo modelo primario: ').strip()
            if model:
                set_primary(model)
                config = load_config()
            elif choice == '4':
                model = input('Nuevo modelo coder: ').strip()
                if model:
                    set_coder(model)
                    config = load_config()
                elif choice == '5':
                    model = input('Nuevo modelo embeddings: ').strip()
                    if model:
                        set_embedding(model)
                        config = load_config()
                    elif choice == '6':
                        param = input('Parámetro (num_ctx/temperature/top_p/repeat_penalty): ').strip()
                        value = input('Valor: ').strip()
                        if param and value:
                            set_param(param, value)
                            config = load_config()
                        elif choice == '7':
                            presets = list_available_presets()
                            print(f'''Presets disponibles: {presets}''')
                            name = input('Nombre del preset: ').strip()
                            if name:
                                apply_preset(name)
                                config = load_config()
                            elif choice == '8':
                                name = input('Nombre para el nuevo preset: ').strip()
                                if name:
                                    save_preset(name)
                                elif choice == '9':
                                    confirm = input('¿Restaurar valores por defecto? (s/n): ').strip().lower()
                                    if confirm == 's':
                                        reset_defaults()
                                        config = load_config()
                                    elif choice == '0':
                                        return None
    continue


def main():
    if len(sys.argv) < 2:
        print('Uso: python -m models.model_config_manager <comando> [args...]')
        print()
        print('Comandos:')
        print('  list                              Ver configuración actual')
        print('  set <agente> <modelo>             Cambiar modelo de un agente')
        print('  primary <modelo>                  Cambiar modelo primario')
        print('  coder <modelo>                    Cambiar modelo coder')
        print('  embedding <modelo>                Cambiar modelo embeddings')
        print('  param <nombre> <valor>            Cambiar parámetro global')
        print('  preset <nombre>                   Aplicar preset de hardware')
        print('  save-preset <nombre>              Guardar config como preset')
        print('  reset                             Restaurar valores por defecto')
        print('  interactive                       Menú interactivo')
        print()
        print('Presets disponibles:')
        print(f'''  {list_available_presets()}''')
        return None
    cmd = sys.argv[1]
    if cmd == 'list':
        list_config()
        return None
    if cmd == 'set':
        if len(sys.argv) < 4:
            print('Uso: set <agente> <modelo>')
            return None
        set_agent_model(sys.argv[2], sys.argv[3])
        return None
    if cmd == 'primary':
        if len(sys.argv) < 3:
            print('Uso: primary <modelo>')
            return None
        set_primary(sys.argv[2])
        return None
    if cmd == 'coder':
        if len(sys.argv) < 3:
            print('Uso: coder <modelo>')
            return None
        set_coder(sys.argv[2])
        return None
    if cmd == 'embedding':
        if len(sys.argv) < 3:
            print('Uso: embedding <modelo>')
            return None
        set_embedding(sys.argv[2])
        return None
    if cmd == 'param':
        if len(sys.argv) < 4:
            print('Uso: param <nombre> <valor>')
            return None
        set_param(sys.argv[2], sys.argv[3])
        return None
    if cmd == 'preset':
        if len(sys.argv) < 3:
            print('Uso: preset <nombre>')
            print(f'''  Presets: {list_available_presets()}''')
            return None
        apply_preset(sys.argv[2])
        return None
    if cmd == 'save-preset':
        if len(sys.argv) < 3:
            print('Uso: save-preset <nombre>')
            return None
        save_preset(sys.argv[2])
        return None
    if cmd == 'reset':
        if len(sys.argv) >= 3 and sys.argv[2] == '-y':
            reset_defaults()
            return None

        try:
            confirm = input('¿Restaurar valores por defecto? (s/n): ').strip().lower()
            if confirm == 's':
                reset_defaults()
                return None
            return None
            if cmd == 'interactive':
                interactive()
                return None
            print(f'''Comando desconocido: {cmd}''')
            sys.exit(1)
            return None
        except EOFError:
            print('Usa: reset -y  para confirmar sin prompt')
            return None


if __name__ == '__main__':
    main()
    return None
