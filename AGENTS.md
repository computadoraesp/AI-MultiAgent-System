<!-- AGENTS.md — Instrucciones concisas para agentes de IA -->
# Instrucciones para agentes (AI coding agents)

Objetivo: ayudar a agentes automáticos a comprender rápidamente la estructura, comandos de ejecución y convenciones del repositorio para ser productivos de inmediato.

Resumen rápido
- **Arranque (API):** `python main.py` → http://localhost:8001
- **Instalación (Windows PowerShell):** `.\setup.ps1` (ver sección PowerShell)
- **Instalación (Linux/macOS):** `chmod +x setup.sh && ./setup.sh`
- **Docker (API + OpenWebUI):** `docker compose -f docker/docker-compose.yml up`
- **Pruebas rápidas:** `python test_run.py`

Archivos clave
- `README.md` — visión general y quick-start ([README.md](README.md)).
- `INSTALL.md` — guía de instalación detallada y presets ([INSTALL.md](INSTALL.md)).
- `setup.ps1` — script de instalación para PowerShell (Windows) ([setup.ps1](setup.ps1)).
- `requirements.txt` — dependencias Python ([requirements.txt](requirements.txt)).
- `main.py` — entrada principal para ejecutar el sistema ([main.py](main.py)).
- `docker/docker-compose.yml` — orquesta servicios (OpenWebUI + API) ([docker/docker-compose.yml](docker/docker-compose.yml)).

Convenciones y supuestos
- **Python 3.12+** es el intérprete objetivo.
- **Ollama** suele usarse como servidor LLM local; los comandos `ollama pull` y `ollama serve` son esperados.
- El proyecto usa presets de modelos: `models/model_config_manager.py` para seleccionar configuraciones por RAM/GPU.
- Memoria dual: JSON + FAISS (repositorio `vectorstore/` y `memory/`).

Qué buscar antes de editar código
- Cambios en `models/model_config.json` o `models/model_config_manager.py` afectan presets y consumo de memoria.
- Cambios en `orchestrator/*` y `planner/*` cambian la ejecución y la generación de tareas.

PowerShell (argumento solicitado)
- Uso recomendado (Windows PowerShell 7+):

```powershell
cd <repo-root>
.\setup.ps1
```

- Flags importantes:
  - `-SkipModels` — omite la descarga automática de modelos.

- Notas para entornos no‑Windows:
  - `pwsh` (PowerShell Core) está disponible en Linux/macOS; ejecutar `pwsh ./setup.ps1` si prefiere PowerShell.
  - En Windows, si ve problemas de encoding: `$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()` (ver `INSTALL.md`).

Comandos útiles que los agentes pueden ejecutar
- Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

- Ejecutar la API localmente:

```bash
python main.py
# luego: curl http://localhost:8001/  o usar test_run.py
```

- Levantar con Docker (API + OpenWebUI):

```bash
docker compose -f docker/docker-compose.yml up
```

Buenas prácticas para PRs automáticos
- Crear commits pequeños y descriptivos; evite cambios masivos en presets sin validación.
- Ejecutar `python -m models.model_config_manager list` después de modificar presets.
- Incluir `test_run.py` al crear PRs que cambien flujo de ejecución.

Enlaces útiles
- Documentación de instalación: [INSTALL.md](INSTALL.md)
- Quick start y arquitectura: [README.md](README.md)

¿Qué más crear?
- Sugerido: una `AGENT-devops.md` con pasos de CI/CD y despliegue automatizado.

---
_Generado automáticamente para ayudar a agentes de IA. Mantener conciso; enlazar documentación existente en lugar de duplicarla._
