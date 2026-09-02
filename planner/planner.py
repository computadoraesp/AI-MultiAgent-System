import os
import json
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from orchestrator.task_schema import Task
from runtime.ollama_manager import OllamaManager
from runtime.json_parser import extract_json

class SubTask(BaseModel):
    task_id: Any = None
    agent: str
    objective: str
    dependencies: List[Any] = Field(default_factory=list)

class Plan(BaseModel):
    subtasks: List[SubTask]

class Planner:
    def __init__(self, llm=None):
        self.llm = llm or OllamaManager()

    def create_plan(self, objective: str) -> List[Task]:
        prompt = f"""
You are a planning agent.

Break the following task into
minimal executable subtasks.

OBJECTIVE:
{objective}

AVAILABLE AGENTS:
- architecture
- backend
- frontend
- ai_deeplearning
- devops
- qa

RULES:
- Return ONLY valid JSON
- Tasks must be atomic
- Prefer parallelizable tasks
- Use dependencies only when necessary

FORMAT:

[
  {{
    "agent": "architecture",
    "objective": "Define system architecture",
    "dependencies": []
  }},
  {{
    "agent": "backend",
    "objective": "Create backend API",
    "dependencies": [
      "Define system architecture"
    ]
  }}
]
"""
        try:
            if hasattr(self.llm, "invoke"):
                import inspect
                sig = inspect.signature(self.llm.invoke)
                if len(sig.parameters) >= 2:
                    result = self.llm.invoke("planner", prompt)
                else:
                    result = self.llm.invoke(prompt)
            else:
                result = self.llm(prompt)

            data = extract_json(str(result))

            if not isinstance(data, list):
                raise ValueError("Planner output must be a list.")

            tasks = []
            objective_to_id = {}

            for item in data:
                task = Task(
                    agent=item.get("agent", "architecture"),
                    objective=item.get("objective", objective),
                    expected_output="implementation",
                    output_format="code"
                )
                objective_to_id[item.get("objective", objective)] = task.task_id
                tasks.append(task)

            for index, item in enumerate(data):
                dependency_ids = []
                for dependency in item.get("dependencies", []):
                    dependency_id = objective_to_id.get(dependency)
                    if dependency_id:
                        dependency_ids.append(dependency_id)
                tasks[index].dependencies = dependency_ids

            return tasks
        except Exception as e:
            print(f"PLANNER ERROR: {str(e)}")
            return [
                Task(
                    agent="architecture",
                    objective=objective,
                    expected_output="implementation",
                    output_format="code"
                )
            ]

def decompose_prompt(objective: str) -> List[dict]:
    planner = Planner()
    tasks = planner.create_plan(objective)
    return [
        {
            "task_id": t.task_id,
            "agent": t.agent,
            "objective": t.objective,
            "dependencies": t.dependencies
        }
        for t in tasks
    ]

def decompose_prompt_structured(objective: str) -> Optional[Plan]:
    try:
        raw_subtasks = decompose_prompt(objective)
        subtasks = [
            SubTask(
                task_id=st["task_id"],
                agent=st["agent"],
                objective=st["objective"],
                dependencies=st.get("dependencies", [])
            )
            for st in raw_subtasks
        ]
        return Plan(subtasks=subtasks)
    except Exception:
        return None
