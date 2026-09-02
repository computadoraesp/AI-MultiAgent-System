# Source Generated with Decompyle++
# File: final_evaluator.cpython-312.pyc (Python 3.12)

import json
from typing import List, Dict, Any, Optional

class FinalEvaluator:

    def __init__(self, runtime):
        self.runtime = runtime


    def evaluate(self = None, original_task = None, agent_outputs = None, conflict_report = (None,)):
        '''
        Evaluates the complete project output against the
        original task and returns a structured veredict.
        '''
        if not agent_outputs:
            return self._empty_veredict(original_task)
        prompt = None._build_prompt(original_task, agent_outputs, conflict_report)
        result = self.runtime.invoke(agent_name = 'qa', prompt = prompt)
        return str(result).strip()


    def _build_prompt(self = None, task = None, outputs = None, conflict_report = ('task', str, 'outputs', List[Dict[(str, str)]], 'conflict_report', Optional[str], 'return', str)):
        lines = []
        for entry in outputs:
            lines.append(f'''AGENT: {entry.get('agent', '?')}''')
            lines.append(f'''OBJECTIVE: {entry.get('objective', '?')}''')
            lines.append(f'''OUTPUT:\n{entry.get('output', '')}''')
        agent_block = '\n\n'.join(lines)
        conflict_block = f'''\nCONFLICT REPORT:\n{conflict_report}''' if conflict_report else '\nCONFLICT REPORT:\nNone detected.'
        return f'''\nYou are a project completion evaluator.\n\nEvaluate the complete multi-agent output below against the\noriginal task requirements. Provide a structured FINAL VEREDICT.\n\nORIGINAL TASK:\n{task}\n\nAGENT OUTPUTS:\n{agent_block}\n\n{conflict_block}\n\nEVALUATION CRITERIA:\n1. COMPLETENESS — What percentage of the original requirements are met?\n2. CORRECTNESS — Does the implementation work logically?\n3. CONSISTENCY — Do the agent outputs fit together coherently?\n4. COVERAGE — Are there missing files, endpoints, or components?\n5. QUALITY — Code quality, error handling, edge cases\n6. INTEGRATION — Do the pieces connect properly (frontend↔backend, API contracts)?\n\nOUTPUT FORMAT (return ONLY this JSON, no other text):\n{{\n  "status": "COMPLETE" | "PARTIAL" | "INCOMPLETE",\n  "completeness_pct": 0-100,\n  "summary": "2-3 sentence overall assessment",\n  "met_requirements": ["requirement 1", "requirement 2"],\n  "missing_requirements": ["missing 1", "missing 2"],\n  "critical_issues": ["issue 1", "issue 2"],\n  "quality_score": "EXCELLENT" | "GOOD" | "FAIR" | "POOR",\n  "recommendations": ["rec 1", "rec 2"]\n}}\n'''


    def _empty_veredict(self = None, task = None):
        return json.dumps({
            'status': 'INCOMPLETE',
            'completeness_pct': 0,
            'summary': 'No agent outputs were generated. The system produced no results.',
            'met_requirements': [],
            'missing_requirements': [
                task],
            'critical_issues': [
                'No outputs from any agent'],
            'quality_score': 'POOR',
            'recommendations': [
                'Check Ollama connectivity',
                'Verify agent prompts',
                'Review system logs'] }, indent = 2)
