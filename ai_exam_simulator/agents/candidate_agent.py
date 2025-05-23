from ai_exam_simulator.core.gemini_client import GeminiClient

class CandidateAgent:
    def __init__(self, agent_id: str, gemini_client: GeminiClient):
        """
        Initializes the Candidate Agent.

        Args:
            agent_id (str): A unique identifier for the agent.
            gemini_client (GeminiClient): An instance of the GeminiClient for LLM interaction.
        """
        self.agent_id = agent_id
        self.gemini_client = gemini_client
        # print(f"CandidateAgent {self.agent_id} initialized.")

    def answer_question(self, question_id: str, question_text: str) -> dict:
        """
        Generates an answer to a given question using the Gemini client.

        Args:
            question_id (str): The ID of the question being answered.
            question_text (str): The text of the question.

        Returns:
            dict: A dictionary containing the question_id, agent_id, and the generated answer.
                  Example: {'question_id': 'q1', 'agent_id': 'c1', 'answer_text': '...'}
        """
        # print(f"CandidateAgent {self.agent_id} received question_id {question_id}: '{question_text[:50]}...'")

        # Construct a prompt for the LLM to answer the question
        # This can be enhanced for more specific instructions or personas
        prompt = f"Question: {question_text}\n\nAnswer:"

        generated_answer_text = self.gemini_client.generate_text(prompt=prompt)

        # print(f"CandidateAgent {self.agent_id} generated answer for question_id {question_id}: '{generated_answer_text[:50]}...'")
        return {
            "question_id": question_id,
            "agent_id": self.agent_id,
            "answer_text": generated_answer_text
        }

if __name__ == '__main__':
    # Example Usage (requires GeminiClient to be functional or mocked)
    # This assumes gemini_client.py is in the parent directory of 'core'
    # Adjust path if necessary for standalone execution, or run from project root.

    # Create a dummy GeminiClient for testing
    class DummyGeminiClient:
        def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
            return f"Dummy answer to: {prompt}"

    # If running this script directly for testing, use a dummy client.
    # For actual simulation, the real GeminiClient (placeholder or actual) will be injected.
    try:
        # Try to import the real client, useful if PYTHONPATH is set (e.g. when run via orchestrator)
        from ai_exam_simulator.core.gemini_client import GeminiClient
        # If a real Gemini API key is available and you want to test with it (even placeholder):
        # gemini_service = GeminiClient(api_key="YOUR_API_KEY")
        # For now, using the placeholder which doesn't need a key
        gemini_service = GeminiClient()
    except ImportError:
        # Fallback to dummy if direct import fails (e.g. running file standalone without project context)
        print("Falling back to DummyGeminiClient for example usage.")
        gemini_service = DummyGeminiClient()


    candidate1 = CandidateAgent(agent_id="candidate001", gemini_client=gemini_service)

    sample_question_id = "math_q1"
    sample_question_text = "What is the Pythagorean theorem and how is it used?"
    
    response = candidate1.answer_question(question_id=sample_question_id, question_text=sample_question_text)

    print(f"--- Example CandidateAgent Usage ---")
    print(f"Agent ID: {response['agent_id']}")
    print(f"Question ID: {response['question_id']}")
    print(f"Question Text: {sample_question_text}")
    print(f"Generated Answer: {response['answer_text']}")
