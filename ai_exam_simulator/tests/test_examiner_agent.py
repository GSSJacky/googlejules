import unittest
from unittest.mock import MagicMock

from ai_exam_simulator.agents.examiner_agent import ExaminerAgent
from ai_exam_simulator.core.gemini_client import GeminiClient # Used for type hinting

class TestExaminerAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.mock_gemini_client = MagicMock(spec=GeminiClient)
        
        self.expected_evaluation_result = {
            "score": 85,
            "feedback": "Mocked feedback: Well structured.",
            "suggestions": "Mocked suggestion: Could add more examples."
        }
        self.mock_gemini_client.evaluate_text.return_value = self.expected_evaluation_result
        
        self.examiner_agent = ExaminerAgent(agent_id="test_examiner_001", gemini_client=self.mock_gemini_client)

    def test_examiner_agent_initialization(self):
        """Test that the ExaminerAgent initializes correctly."""
        self.assertEqual(self.examiner_agent.agent_id, "test_examiner_001")
        self.assertEqual(self.examiner_agent.gemini_client, self.mock_gemini_client)

    def test_evaluate_answer_calls_gemini_client(self):
        """Test that evaluate_answer calls gemini_client.evaluate_text with the correct structure."""
        question_id = "q_eval_01"
        question_text = "Explain the concept of photosynthesis."
        candidate_answer = "It's how plants make food using sunlight."
        model_answer = "Photosynthesis is a process used by plants..." # Optional

        self.examiner_agent.evaluate_answer(
            question_id=question_id,
            question_text=question_text,
            candidate_answer_text=candidate_answer,
            model_answer_text=model_answer
        )
        
        # Verify that evaluate_text was called once.
        # We'll check the first argument (prompt) more loosely, as it's complex.
        # The key is that it *is* called.
        self.mock_gemini_client.evaluate_text.assert_called_once()
        
        # Grab the actual call arguments
        call_args = self.mock_gemini_client.evaluate_text.call_args[1] # keyword arguments
        
        # Check that the important parts are in the prompt sent to Gemini
        self.assertIn(question_text, call_args['prompt'])
        self.assertIn(candidate_answer, call_args['prompt'])
        self.assertIn(model_answer, call_args['prompt'])
        self.assertIn("Structure your response as a JSON object", call_args['prompt']) # Check for instructions

    def test_evaluate_answer_returns_correct_format(self):
        """Test that evaluate_answer returns a dictionary in the expected format."""
        question_id = "q_eval_02"
        question_text = "What is gravity?"
        candidate_answer = "It's what keeps us on the ground."
        
        result = self.examiner_agent.evaluate_answer(
            question_id=question_id,
            question_text=question_text,
            candidate_answer_text=candidate_answer
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("question_id", result)
        self.assertEqual(result["question_id"], question_id)
        self.assertIn("evaluator_agent_id", result)
        self.assertEqual(result["evaluator_agent_id"], self.examiner_agent.agent_id)
        self.assertIn("candidate_answer_text", result)
        self.assertEqual(result["candidate_answer_text"], candidate_answer)
        self.assertIn("evaluation", result)
        self.assertEqual(result["evaluation"], self.expected_evaluation_result)

    def test_evaluate_answer_without_model_answer(self):
        """Test evaluate_answer when no model answer is provided."""
        question_id = "q_eval_03"
        question_text = "Define AI."
        candidate_answer = "Artificial Intelligence."

        self.examiner_agent.evaluate_answer(
            question_id=question_id,
            question_text=question_text,
            candidate_answer_text=candidate_answer,
            model_answer_text=None # Explicitly None
        )

        self.mock_gemini_client.evaluate_text.assert_called_once()
        call_args = self.mock_gemini_client.evaluate_text.call_args[1]
        self.assertIn(question_text, call_args['prompt'])
        self.assertIn(candidate_answer, call_args['prompt'])
        self.assertNotIn("Model Answer is provided below", call_args['prompt'])


if __name__ == '__main__':
    # python -m unittest ai_exam_simulator/tests/test_examiner_agent.py
    unittest.main()
