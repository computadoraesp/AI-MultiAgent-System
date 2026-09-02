from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from orchestrator.orchestrator import run_multiagent_system, run_project_audit, run_github_clone, run_construct_with_push
from orchestrator.prompt_analyzer import analyze_prompt

router = APIRouter()

class ExecuteRequest(BaseModel):
    task: Optional[str] = None
    mode: Optional[str] = "construct"
    project_path: Optional[str] = None
    auto_approve: bool = True
    github_token: Optional[str] = None
    github_repo: Optional[str] = None
    github_action: Optional[str] = None

class ExecuteResponse(BaseModel):
    mode: str
    result: str
    project_path: Optional[str] = None
    task: Optional[str] = None
    github_action: Optional[str] = None
    github_url: Optional[str] = None

@router.post("/execute", response_model=ExecuteResponse)
def execute_task(request: ExecuteRequest):
    raw_prompt = request.task or ""
    if request.project_path and not raw_prompt:
        raw_prompt = request.project_path

    analyzed = analyze_prompt(raw_prompt)

    github_action = request.github_action or analyzed.github_action
    project_path = request.project_path or analyzed.project_path
    mode = request.mode if request.mode != "construct" else analyzed.mode
    task_str = request.task or analyzed.task

    if github_action == "clone":
        if not project_path:
            return ExecuteResponse(
                mode="review",
                result="Error: project_path (GitHub URL) is required for clone"
            )
        output = run_github_clone(
            repo_url=project_path,
            instructions=task_str,
            github_token=request.github_token,
            auto_approve=request.auto_approve
        )
        return ExecuteResponse(
            mode="review",
            result=output,
            project_path=project_path,
            github_action="clone",
            github_url=project_path
        )

    if github_action == "push" or request.github_repo or analyzed.github_repo:
        repo_name = request.github_repo or analyzed.github_repo or "ai-generated-project"
        output = run_construct_with_push(
            task=task_str,
            repo_name=repo_name,
            github_token=request.github_token
        )
        return ExecuteResponse(
            mode="construct",
            result=output,
            github_action="push",
            github_repo=repo_name
        )

    if mode == "review":
        if not project_path:
            return ExecuteResponse(
                mode="review",
                result="Error: project_path is required for review mode"
            )
        result = run_project_audit(
            project_path=project_path,
            instructions=task_str,
            auto_approve=request.auto_approve
        )
        return ExecuteResponse(
            mode="review",
            result=result,
            project_path=project_path
        )

    result = run_multiagent_system(task_str)
    return ExecuteResponse(
        mode="construct",
        result=result,
        task=task_str
    )
