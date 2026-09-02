import os
import sys
import json
import shutil
import subprocess
from typing import Dict, Any, Optional
from copy import deepcopy

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_PATH, "models", "model_config.json")
PRESETS_PATH = os.path.join(BASE_PATH, "models", "presets")

def detect_hardware_specs() -> Dict[str, Any]:
    ram_gb = 16.0
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    except Exception:
        try:
            if sys.platform != "win32":
                mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
                ram_gb = mem_bytes / (1024 ** 3)
        except Exception:
            pass

    cpu_cores = os.cpu_count() or 4

    has_gpu = False
    vram_gb = 0.0
    try:
        res = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            vram_mb = float(res.stdout.strip().split("\n")[0])
            vram_gb = vram_mb / 1024.0
            has_gpu = True
    except Exception:
        pass

    return {
        "ram_gb": round(ram_gb, 1),
        "cpu_cores": cpu_cores,
        "has_gpu": has_gpu,
        "vram_gb": round(vram_gb, 1)
    }

def auto_select_preset_for_hardware() -> str:
    specs = detect_hardware_specs()
    ram = specs["ram_gb"]
    gpu = specs["has_gpu"]
    vram = specs["vram_gb"]

    if ram >= 28 or (gpu and vram >= 8):
        return "high_gpu"
    elif ram >= 12:
        return "medium"
    else:
        return "low_ram"

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        preset = auto_select_preset_for_hardware()
        apply_preset(preset)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config: Dict[str, Any]) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_ollama_models() -> list:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        lines = result.stdout.strip().split("\n")
        models = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                m = parts[0].replace(":latest", "")
                models.append(m)
        return models
    except Exception:
        return []

def list_config():
    config = load_config()
    specs = detect_hardware_specs()
    print("\n=== ESPECIFICACIONES DE HARDWARE ===")
    print(f"  RAM detectada:      {specs['ram_gb']} GB")
    print(f"  Cores CPU:          {specs['cpu_cores']}")
    print(f"  GPU NVIDIA:         {'Sí (' + str(specs['vram_gb']) + ' GB VRAM)' if specs['has_gpu'] else 'No/No detectada'}")
    print(f"  Preset sugerido:    {auto_select_preset_for_hardware()}")

    print("\n=== CONFIGURACIÓN ACTUAL ===\n")
    print("  Modelo primario:     ", config.get("primary_model"))
    print("  Modelo coder:        ", config.get("coder_model"))
    print("  Modelo fallback:     ", config.get("fallback_model"))
    print("  Modelo embeddings:   ", config.get("embedding_model"))
    print("\n  Agentes:")
    for agent, model in config.get("agent_models", {}).items():
        print(f"    {agent:15s} -> {model}")
    print("\n  Parámetros:")
    for k, v in config.get("params", {}).items():
        print(f"    {k:20s} = {v}")

def set_agent_model(agent: str, model_name: str):
    config = load_config()
    if "agent_models" not in config:
        config["agent_models"] = {}
    config["agent_models"][agent] = model_name
    save_config(config)
    print(f"OK: Agente '{agent}' actualizado a '{model_name}'")

def set_primary(model_name: str):
    config = load_config()
    config["primary_model"] = model_name
    save_config(config)
    print(f"OK: Modelo primario actualizado a '{model_name}'")

def set_coder(model_name: str):
    config = load_config()
    config["coder_model"] = model_name
    save_config(config)
    print(f"OK: Modelo coder actualizado a '{model_name}'")

def set_embedding(model_name: str):
    config = load_config()
    config["embedding_model"] = model_name
    save_config(config)
    print(f"OK: Modelo embeddings actualizado a '{model_name}'")

def set_param(param: str, value: str):
    config = load_config()
    if "params" not in config:
        config["params"] = {}

    val: Any = value
    if value.lower() in ["true", "false"]:
        val = value.lower() == "true"
    else:
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                val = value

    config["params"][param] = val
    save_config(config)
    print(f"OK: Parámetro '{param}' actualizado a {val}")

def apply_preset(name: str):
    preset_path = os.path.join(PRESETS_PATH, f"{name}.json")
    if not os.path.exists(preset_path):
        print(f"ERROR: Preset '{name}' no encontrado.")
        print(f"  Presets disponibles: {list_available_presets()}")
        return
    with open(preset_path, "r", encoding="utf-8") as f:
        preset = json.load(f)
    desc = preset.pop("description", "")
    save_config(preset)
    print(f"OK: Preset '{name}' aplicado")
    if desc:
        print(f"  Descripción: {desc}")

def auto_tune_hardware():
    preset = auto_select_preset_for_hardware()
    apply_preset(preset)
    print(f"OK: Sistema ajustado automáticamente al preset '{preset}'.")

def list_available_presets() -> list:
    if not os.path.exists(PRESETS_PATH):
        return []
    presets = []
    for f in os.listdir(PRESETS_PATH):
        if f.endswith(".json"):
            presets.append(f[:-5])
    return sorted(presets)

def save_preset(name: str):
    os.makedirs(PRESETS_PATH, exist_ok=True)
    config = load_config()
    config["description"] = f"Preset guardado como {name}"
    preset_path = os.path.join(PRESETS_PATH, f"{name}.json")
    with open(preset_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"OK: Preset guardado en {preset_path}")

def reset_defaults():
    auto_tune_hardware()

def interactive():
    while True:
        print("\n--- Model Config Manager ---")
        print("1) Ver configuración y hardware")
        print("2) Cambiar modelo de un agente")
        print("3) Cambiar modelo primario")
        print("4) Cambiar modelo coder")
        print("5) Aplicar preset")
        print("6) Ajustar automáticamente según Hardware")
        print("7) Ver modelos en Ollama")
        print("0) Salir")
        choice = input("Opción: ").strip()
        if choice == "1":
            list_config()
        elif choice == "2":
            agent = input("Nombre del agente: ").strip()
            model = input("Nombre del modelo: ").strip()
            if agent and model:
                set_agent_model(agent, model)
        elif choice == "3":
            model = input("Modelo primario: ").strip()
            if model:
                set_primary(model)
        elif choice == "4":
            model = input("Modelo coder: ").strip()
            if model:
                set_coder(model)
        elif choice == "5":
            print(f"Presets: {list_available_presets()}")
            preset = input("Nombre del preset: ").strip()
            if preset:
                apply_preset(preset)
        elif choice == "6":
            auto_tune_hardware()
        elif choice == "7":
            models = get_ollama_models()
            print("Modelos Ollama instalados:")
            for m in models:
                print(f"  - {m}")
        elif choice == "0":
            break

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m models.model_config_manager <comando> [args...]")
        print("Comandos:")
        print("  list                              Ver configuración actual")
        print("  autotune                          Ajuste automático según Hardware")
        print("  set <agente> <modelo>             Cambiar modelo de un agente")
        print("  primary <modelo>                  Cambiar modelo primario")
        print("  coder <modelo>                    Cambiar modelo coder")
        print("  embedding <modelo>                Cambiar modelo embeddings")
        print("  param <nombre> <valor>            Cambiar parámetro global")
        print("  preset <nombre>                   Aplicar preset de hardware")
        print("  save-preset <nombre>              Guardar config como preset")
        print("  reset                             Restaurar valores por defecto")
        print("  interactive                       Menú interactivo")
        print("\nPresets disponibles:")
        print("  ", list_available_presets())
        return

    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_config()
    elif cmd == "autotune":
        auto_tune_hardware()
    elif cmd == "set":
        if len(sys.argv) < 4:
            print("Uso: set <agente> <modelo>")
            return
        set_agent_model(sys.argv[2], sys.argv[3])
    elif cmd == "primary":
        if len(sys.argv) < 3:
            print("Uso: primary <modelo>")
            return
        set_primary(sys.argv[2])
    elif cmd == "coder":
        if len(sys.argv) < 3:
            print("Uso: coder <modelo>")
            return
        set_coder(sys.argv[2])
    elif cmd == "embedding":
        if len(sys.argv) < 3:
            print("Uso: embedding <modelo>")
            return
        set_embedding(sys.argv[2])
    elif cmd == "param":
        if len(sys.argv) < 4:
            print("Uso: param <nombre> <valor>")
            return
        set_param(sys.argv[2], sys.argv[3])
    elif cmd == "preset":
        if len(sys.argv) < 3:
            print("Uso: preset <nombre>")
            print(f"  Presets: {list_available_presets()}")
            return
        apply_preset(sys.argv[2])
    elif cmd == "save-preset":
        if len(sys.argv) < 3:
            print("Uso: save-preset <nombre>")
            return
        save_preset(sys.argv[2])
    elif cmd == "reset":
        if len(sys.argv) >= 3 and sys.argv[2] == "-y":
            reset_defaults()
            return
        try:
            confirm = input("¿Restaurar valores por defecto? (s/n): ").strip().lower()
            if confirm == "s":
                reset_defaults()
        except EOFError:
            print("Usa: reset -y  para confirmar sin prompt")
    elif cmd == "interactive":
        interactive()
    else:
        print(f"Comando desconocido: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
