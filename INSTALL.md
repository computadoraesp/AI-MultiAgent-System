# Installation Guide — Multi-Agent RAG System

## Prerequisites

| Program | Version | Download |
|---------|---------|----------|
| Python | 3.12+ | https://www.python.org/downloads/ |
| Ollama | 0.3+ | https://ollama.com/download |
| Docker (optional) | 24+ | https://www.docker.com/products/docker-desktop/ |

---

## Step 1: Install Ollama and pull models

```bash
# Download recommended models
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b-instruct-q4_K_M
ollama pull phi3:mini
```

Verify Ollama is running:
```bash
ollama list
# Should show downloaded models
```

---

## Step 2: Clone / prepare the project

```bash
cd AI-MultiAgent-System
```

---

## Step 3: Run the setup script

### Windows (PowerShell 7+)

```powershell
.\setup.ps1
```

The script will:
1. Verify Python  
2. Install dependencies (`pip install -r requirements.txt`)  
3. Create required directories (`logs/`, `memory/`, `vectorstore/`, etc.)  
4. Verify Ollama is installed and running  
5. Optionally download recommended models  
6. Show locally available models  

### Linux / macOS

```bash
chmod +x setup.sh
./setup.sh
```

---

## Step 4: Configure models for your hardware

The system includes hardware presets. Choose the one matching your machine:

### 8GB RAM (low-end)

```bash
python -m models.model_config_manager preset low_ram
```

### 16GB RAM (mid-range) — default

```bash
python -m models.model_config_manager preset medium
```

### 32GB+ RAM with GPU (high-end)

```bash
python -m models.model_config_manager preset high_gpu
```

### Configure the planner model

```bash
# View current planner model
python -m models.model_config_manager list

# Change planner model
python -m models.model_config_manager set planner llama3.1:8b
```

### Manual configuration

```bash
python -m models.model_config_manager interactive
python -m models.model_config_manager list
python -m models.model_config_manager set backend deepseek-coder:14b
python -m models.model_config_manager param temperature 0.15
```

---

## Step 5: Start the system

### Option A — API only (fastest)

```bash
python main.py
# → http://localhost:8001
# Docs: http://localhost:8001/docs
```

### Option B — API + OpenWebUI (with Docker)

```bash
docker compose -f docker/docker-compose.yml up
# → API:        http://localhost:8001
# → OpenWebUI:  http://localhost:3000
```

### Option C — Everything without Docker

```bash
# Terminal 1: API
python main.py

# Terminal 2: OpenWebUI
pip install open-webui
open-webui serve
# → http://localhost:8080
```

---

## Verify it works

```bash
curl http://localhost:8001/
# → {"status": "running", "system": "AI MultiAgent System"}

curl -X POST http://localhost:8001/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a Python script that prints hello world"}'
```

Or use the test script:

```bash
python test_run.py
```

---

## Troubleshooting

### "Ollama server is not running"

```bash
ollama serve
```

### "Model not found"

```bash
ollama list
ollama pull llama3.1:8b
```

### Out of memory

1. Apply low RAM preset:  
   ```bash
   python -m models.model_config_manager preset low_ram
   ```
2. Reduce context size:  
   ```bash
   python -m models.model_config_manager param num_ctx 2048
   ```

### Encoding issues on Windows

```powershell
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
```

---

## GitHub Integration

The system can clone GitHub repositories and push generated projects. Everything is on-demand.

### Push — Upload generated project to GitHub

Example:

```
"Create a REST API with Flask and push it to GitHub as flask-api"
```

Flow:
1. Build project  
2. Init git  
3. Commit  
4. Create repo via GitHub API  
5. Push  

Requires GitHub token:

```json
{
  "task": "Create a REST API with Flask",
  "github_repo": "flask-api",
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Clone — Clone repository and audit

Example:

```
"Clone https://github.com/user/blog and add JWT login"
```

Flow:
1. Detect GitHub URL  
2. Clone repo  
3. Review mode  
4. Apply improvements  

---

## OpenWebUI Integration

### Configuration

1. OpenWebUI → Admin Panel → Connections → OpenAI  
2. API URL:  
   - Docker: `http://host.docker.internal:8001/v1`  
   - Local: `http://localhost:8001/v1`  
3. API Key: *(leave empty)*  
4. Save  

### Automatic mode detection

| Prompt | Mode |
|--------|------|
| "create a REST API with Flask" | construct |
| "review C:/my-project" | review |
| "continue output/projects/... add login" | continue |

### Test

```bash
curl http://localhost:8001/v1/models
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"multiagent-system","messages":[{"role":"user","content":"hello"}]}'
```

---

## Recent Changes

- Semantic routing using FAISS + Sentence-Transformers  
- Dedicated planner model  
- Conflict detection across all agent outputs  
- Final structured verdict with completion %, issues, recommendations  
