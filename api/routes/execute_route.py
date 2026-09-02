from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from orchestrator.orchestrator import run_multiagent_system, run_project_audit, run_github_clone, run_construct_with_push

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
    if request.github_action == "clone":
        if not request.project_path:
            return ExecuteResponse(
                mode="review",
                result="Error: project_path (GitHub URL) is required for clone"
            )
        output = run_github_clone(
            repo_url=request.project_path,
            instructions=request.task,
            github_token=request.github_token,
            auto_approve=request.auto_approve
        )
        return ExecuteResponse(
            mode="review",
            result=output,
            project_path=request.project_path,
            github_action="clone",
            github_url=request.project_path
        )

    if request.github_action == "push" or request.github_repo:
        output = run_construct_with_push(
            task=request.task,
            repo_name=request.github_repo or "ai-generated-project",
            github_token=request.github_token
        )
        return ExecuteResponse(
            mode="construct",
            result=output,
            github_action="push",
            github_repo=request.github_repo
        )

    if request.mode == "review":
        if not request.project_path:
            return ExecuteResponse(
                mode="review",
                result="Error: project_path is required for review mode"
            )
        result = run_project_audit(
            project_path=request.project_path,
            instructions=request.task,
            auto_approve=request.auto_approve
        )
        return ExecuteResponse(
            mode="review",
            result=result,
            project_path=request.project_path
        )

    result = run_multiagent_system(request.task)
    return ExecuteResponse(
        mode="construct",
        result=result,
        task=request.task
    )
