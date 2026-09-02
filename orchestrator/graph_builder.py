# Source Generated with Decompyle++
# File: graph_builder.cpython-312.pyc (Python 3.12)

from langgraph.graph import StateGraph, END
from orchestrator.graph_nodes import OrchestratorState, orchestrator_step, agent_step, qa_step, retry_step, save_step, qa_router

def build_agent_graph():
    workflow = StateGraph(OrchestratorState)
    workflow.add_node('orchestrator', orchestrator_step)
    workflow.add_node('agent', agent_step)
    workflow.add_node('qa', qa_step)
    workflow.add_node('retry', retry_step)
    workflow.add_node('save', save_step)
    workflow.set_entry_point('orchestrator')
    workflow.add_edge('orchestrator', 'agent')
    workflow.add_edge('agent', 'qa')
    workflow.add_conditional_edges('qa', qa_router, {
        'retry': 'retry',
        'save': 'save' })
    workflow.add_edge('retry', 'qa')
    workflow.add_edge('save', END)
    return workflow.compile()
