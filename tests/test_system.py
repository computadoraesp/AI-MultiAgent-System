import unittest
from planner.planner import decompose_prompt, decompose_prompt_structured
from orchestrator.permission_manager import check_permission
from orchestrator.prompt_analyzer import analyze_prompt
from runtime.output_parser import parse_agent_output, parse_qa_output

class TestSystem(unittest.TestCase):
    def test_planner_decomposition(self):
        task = "Build a REST API with FastAPI and SQLite"
        subtasks = decompose_prompt(task)
        self.assertIsInstance(subtasks, list)
        self.assertGreater(len(subtasks), 0)

        plan = decompose_prompt_structured(task)
        self.assertIsNotNone(plan)
        self.assertGreater(len(plan.subtasks), 0)

    def test_permission_manager(self):
        allowed, msg = check_permission("backend", "Create backend API endpoints")
        self.assertTrue(allowed)

    def test_prompt_analyzer(self):
        res = analyze_prompt("Create a Flask API")
        self.assertEqual(res.mode, "construct")
        self.assertEqual(res.task, "Create a Flask API")

        res_review = analyze_prompt("Review output/projects/test")
        self.assertEqual(res_review.mode, "review")

    def test_output_parser(self):
        raw_text = '{"summary": "Created API", "files": [{"path": "main.py", "content": "print(1)"}]}'
        parsed = parse_agent_output(raw_text)
        self.assertEqual(parsed["summary"], "Created API")
        self.assertEqual(len(parsed["files"]), 1)

        qa_raw = "STATUS: APPROVED\nISSUES: None\nRECOMMENDATIONS: None"
        parsed_qa = parse_qa_output(qa_raw)
        self.assertEqual(parsed_qa["status"], "APPROVED")

if __name__ == "__main__":
    unittest.main()
