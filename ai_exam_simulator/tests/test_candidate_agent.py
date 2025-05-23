import unittest
from unittest.mock import MagicMock

# Assuming the project root is in PYTHONPATH for ai_exam_simulator imports
from ai_exam_simulator.agents.candidate_agent import CandidateAgent
from ai_exam_simulator.core.gemini_client import GeminiClient # Used for type hinting

class TestCandidateAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        # Create a mock GeminiClient
        self.mock_gemini_client = MagicMock(spec=GeminiClient)
        
        # Configure the mock's generate_text method to return a specific value
        self.expected_answer = "Mocked Gemini answer for test."
        self.mock_gemini_client.generate_text.return_value = self.expected_answer
        
        # Instantiate CandidateAgent with the mock client
        self.candidate_agent = CandidateAgent(agent_id="test_candidate_001", gemini_client=self.mock_gemini_client)

    def test_candidate_agent_initialization(self):
        """Test that the CandidateAgent initializes correctly."""
        self.assertEqual(self.candidate_agent.agent_id, "test_candidate_001")
        self.assertEqual(self.candidate_agent.gemini_client, self.mock_gemini_client)

    def test_answer_question_calls_gemini_client(self):
        """Test that answer_question method calls gemini_client.generate_text."""
        question_id = "q_test_01"
        question_text = "This is a test question?"
        
        self.candidate_agent.answer_question(question_id=question_id, question_text=question_text)
        
        # Verify that generate_text was called once with the correct prompt
        expected_prompt = f"Question: {question_text}\n\nAnswer:"
        self.mock_gemini_client.generate_text.assert_called_once_with(prompt=expected_prompt)

    def test_answer_question_returns_correct_format(self):
        """Test that answer_question returns a dictionary in the expected format."""
        question_id = "q_test_02"
        question_text = "Another test question."
        
        result = self.candidate_agent.answer_question(question_id=question_id, question_text=question_text)
        
        self.assertIsInstance(result, dict)
        self.assertIn("question_id", result)
        self.assertIn("agent_id", result)
        self.assertIn("answer_text", result)
        
        self.assertEqual(result["question_id"], question_id)
        self.assertEqual(result["agent_id"], self.candidate_agent.agent_id)
        self.assertEqual(result["answer_text"], self.expected_answer)

if __name__ == '__main__':
    # To run tests from the command line from the project root:
    # python -m unittest ai_exam_simulator/tests/test_candidate_agent.py
    # Or, to discover all tests in the 'tests' directory:
    # python -m unittest discover -s ai_exam_simulator/tests -p "test_*.py"
    unittest.main()
