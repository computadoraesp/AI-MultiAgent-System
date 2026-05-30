# Multi-Agent RAG System

A 100% local multi-agent software engineering system. It receives a natural language task, decomposes it, assigns specialized AI agents, generates code, validates, detects cross-agent conflicts, and produces a structured verdict — all offline.

## Architecture

```
User → [Planner] → [TaskGraph (dependencies)]
                            │
              ┌─────────────┼─────────────┐
              ▼ (ThreadPool 4 workers)    ▼
         [Orchestrator Step]   ...   [Orchestrator Step]
              │                           │
              ▼                           ▼
         [Agent Step]               [Agent Step]
              │                           │
              ▼                           ▼
          [QA Step]                   [QA Step]
              │                           │
         ┌────┴────┐                ┌────┴────┐
         ▼         ▼                ▼         ▼
      [Retry]   [Save → Memory]   [Retry]  [Save → Memory]
              │                           │
              └──────────┬────────────────┘
                         ▼
              [ConflictDetector]  ← cross-checks agent outputs
                         │
                         ▼
              [FinalEvaluator]   ← structured verdict
                         │
                         ▼
                 FINAL RESULT
```

## Pipeline

| Step | Component | File |
|------|-----------|------|
| 1 | Planner breaks task into atomic subtasks | `planner/planner.py` |
| 2 | TaskGraph resolves dependencies | `orchestrator/task_graph.py` |
| 3 | ThreadPool executes ready tasks in parallel | `orchestrator/orchestrator.py` |
| 4 | Orchestrator queries memory + analysis | `orchestrator/graph_nodes.py` |
| 5 | Agent executes subtask via LLM | `orchestrator/graph_nodes.py` |
| 6 | QA validates individual output | `orchestrator/graph_nodes.py` |
| 7 | Retry (up to 2 attempts if QA rejects) | `orchestrator/graph_nodes.py` |
| 8 | Save to dual memory (JSON + FAISS) | `runtime/persistence_manager.py` |
| 9 | ConflictDetector cross-checks all agent outputs | `orchestrator/conflict_detector.py` |
| 10 | FinalEvaluator produces structured verdict | `orchestrator/final_evaluator.py` |

## Agents

| Agent | Default Model | Role |
|-------|--------------|------|
| **planner** | `llama3.1:8b` | Breaks task into subtasks with dependencies |
| **orchestrator** | `llama3.1:8b` | Coordinates, queries memory, provides context |
| **architecture** | `llama3.1:8b` | Designs system architecture |
| **backend** | `deepseek-coder:6.7b` | Generates backend code (APIs, models, DB) |
| **frontend** | `deepseek-coder:6.7b` | Generates frontend code (UI, components) |
| **ai_deeplearning** | `deepseek-coder:6.7b` | ML/DL pipelines, RAG, embeddings |
| **devops** | `deepseek-coder:6.7b` | Docker, CI/CD, infrastructure |
| **qa** | `llama3.1:8b` | Validation, error detection, conflict checking |

## Agent Communication

Agents **do not talk to each other directly**. They use a **shared blackboard** pattern:

1. Each agent saves its output to dual memory (JSON + FAISS)
2. Subsequent agents retrieve prior outputs via semantic search
3. `ConflictDetector` actively compares all outputs at the end
4. No direct messaging between agents

## GitHub Integration

The system supports two GitHub flows, both **on-demand** (never connects without explicit user request):

| Action | Prompt detection | Flow |
|--------|-----------------|------|
| **Push** | `"push to GitHub as <repo>"` | Build offline → git init → commit → create repo → push |
| **Clone** | `"clone https://github.com/..."` | git clone → review code → apply improvements |

For private repos, provide a GitHub Personal Access Token (`ghp_...`) as an optional parameter.

See `INSTALL.md` → "GitHub Integration" for details.

## Tech Stack

- **Python 3.12+** — Base language
- **Ollama** — Local LLM server
- **LangGraph** — Agent flow orchestration with state graphs
- **LangChain** — LLM framework
- **FAISS** — Vector memory (semantic search)
- **Sentence-Transformers** — Embeddings for semantic agent routing
- **FastAPI** — REST API
- **OpenWebUI** — Optional web interface
- **ThreadPoolExecutor** — Parallel agent execution

## Minimum Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| Disk | 15 GB free | 30 GB |
| GPU | Not required | NVIDIA 6GB+ VRAM |
| OS | Windows / Linux / macOS | Windows / Linux |

## Quick Start

```bash
# 1. Install Ollama (https://ollama.com/download)

# 2. Pull models
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b

# 3. Run setup
.\setup.ps1          # Windows
# bash setup.sh      # Linux/Mac

# 4. Configure model preset for your hardware
python -m models.model_config_manager preset medium

# 5. Start the system
python main.py
# → http://localhost:8001

# 6. Test with an example
python test_run.py
```

## OpenWebUI Integration

OpenWebUI can connect to the multi-agent system as an **external OpenAI provider**.

### Docker Setup

With `docker compose -f docker/docker-compose.yml up`, the API is at `http://host.docker.internal:8001`.  
In OpenWebUI:

1. **Admin Settings → Connections → OpenAI**
2. **URL**: `http://host.docker.internal:8001/v1`
3. **API Key**: *(leave empty)*
4. **Save**

The `multiagent-system` model will appear in the chat dropdown.

### Behavior

| Prompt in OpenWebUI | Detected mode |
|---|---|
| `"create a REST API with Flask"` | `construct` — builds from scratch |
| `"review C:/my-project and improve the code"` | `review` — audits existing project |
| `"continue output/projects/... add login"` | `continue` — resumes previous project |

### Exposed Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /v1/models` | OpenWebUI discovers available model |
| `POST /v1/chat/completions` | Full chat with automatic mode detection |
| `POST /execute` | Direct API with explicit mode control |

## Documentation

- [Detailed installation guide](INSTALL.md)
- [Model configuration](models/model_config_manager.py)

## License

MIT
