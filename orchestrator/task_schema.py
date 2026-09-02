import uuid
from typing import Dict, List, Literal, Any, Optional
from pydantic import BaseModel, Field

AgentType = Literal['architecture', 'backend', 'frontend', 'ai_deeplearning', 'devops', 'qa', 'planner', 'orchestrator']
OutputFormat = Literal['code', 'json', 'report', 'architecture']
PriorityLevel = Literal['low', 'medium', 'high']

class TaskContext(BaseModel):
    requirements: List[str] = Field(default_factory=list)
    files: List[str] = Field(default_factory=list)
    memory: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Task(BaseModel):
    task_id: Any = Field(default_factory=lambda: str(uuid.uuid4()))
    agent: str = Field(default="architecture")
    objective: str = Field(min_length=3)
    dependencies: List[Any] = Field(default_factory=list, description="Task IDs or objectives required before execution")
    context: TaskContext = Field(default_factory=TaskContext)
    expected_output: str = Field(default="implementation")
    output_format: str = Field(default="code")
    priority: str = Field(default="medium")
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=2, ge=1)
    parent_task_id: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)

class TaskResponse(BaseModel):
    status: Literal['success', 'failed', 'needs_clarification'] = 'success'
    result: Dict[str, Any] = Field(default_factory=dict)
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    execution_time: Optional[float] = None
    memory_saved: bool = False
    retry_recommended: bool = False
