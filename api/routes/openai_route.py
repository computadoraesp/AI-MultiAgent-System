import time
import logging
from typing import List, Optional, Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from orchestrator.orchestrator import run_multiagent_system, run_project_audit, run_github_clone, run_construct_with_push
from orchestrator.prompt_analyzer import analyze_prompt

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "multiagent-system"
    messages: List[ChatMessage]
    stream: Optional[bool] = False

@router.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "multiagent-system",
                "object": "model",
                "created": 1700000000,
                "owned_by": "local-system"
            }
        ]
    }

@router.post("/v1/chat/completions")
def chat_completion(request: ChatCompletionRequest):
    if not request.messages:
        return _openai_response("No messages provided.", request.model)

    last_msg = request.messages[-1]
    prompt = last_msg.content.strip()

    if prompt.lower() in ["ping", "hello", "hola"]:
        return _openai_response("Sistema multi-agente listo. Envíame una tarea.", request.model)

    analysis = analyze_prompt(prompt)
    logger.info("Prompt analyzed: mode=%s path=%s task=%.60s", analysis.mode, analysis.project_path, analysis.task)

    try:
        if analysis.github_action == "clone":
            output = run_github_clone(
                repo_url=analysis.project_path,
                instructions=analysis.task,
                auto_approve=True
            )
            result = {
                "mode": "review",
                "github_action": "clone",
                "github_url": analysis.github_url,
                "result": output
            }
        elif analysis.github_action == "push":
            output = run_construct_with_push(
                task=analysis.task,
                repo_name=analysis.github_repo or "ai-generated-project"
            )
            result = {
                "mode": "construct",
                "github_action": "push",
                "github_repo": analysis.github_repo,
                "result": output
            }
        elif analysis.mode == "review":
            if not analysis.project_path:
                result = {
                    "error": "project_path is required for review mode",
                    "analysis": analysis.to_dict()
                }
            else:
                output = run_project_audit(
                    project_path=analysis.project_path,
                    instructions=analysis.task,
                    auto_approve=True
                )
                result = {
                    "mode": "review",
                    "project_path": analysis.project_path,
                    "result": output
                }
        elif analysis.mode == "continue":
            if not analysis.project_path:
                result = {
                    "error": "project_path is required for continue mode",
                    "analysis": analysis.to_dict()
                }
            else:
                output = run_project_audit(
                    project_path=analysis.project_path,
                    instructions=analysis.task,
                    auto_approve=True
                )
                result = {
                    "mode": "continue",
                    "project_path": analysis.project_path,
                    "result": output
                }
        else:
            output = run_multiagent_system(prompt)
            result = {
                "mode": "construct",
                "task": analysis.task,
                "result": output
            }
    except Exception as e:
        logger.exception("Execution failed")
        result = {
            "error": str(e),
            "mode": analysis.mode
        }

    content = _format_result(result)
    return _openai_response(content, request.model)

def _format_result(result: Dict[str, Any]) -> str:
    if "error" in result:
        return f"Error ({result.get('mode', 'unknown')}): {result['error']}"

    github_action = result.get("github_action")
    if github_action == "clone":
        body = result.get("result", "")
        url = result.get("github_url", "")
        return f"## Clonado + Review: {url}\n\n{body}"

    if github_action == "push":
        body = result.get("result", "")
        repo = result.get("github_repo", "")
        return f"## Construcción + GitHub Push: {repo}\n\n{body}"

    if result["mode"] == "construct":
        body = result.get("result", "")
        return f"## Construcción completada\n\n{body}"

    mode_label = "Review" if result["mode"] == "review" else "Continuación"
    body = result.get("result", "")
    project = result.get("project_path", "")
    return f"## {mode_label}: {project}\n\n{body}"

def _openai_response(content: str, model: str) -> Dict[str, Any]:
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
