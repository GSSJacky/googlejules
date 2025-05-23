from ai_exam_simulator.core.gemini_client import GeminiClient

class ExaminerAgent:
    def __init__(self, agent_id: str, gemini_client: GeminiClient):
        """
        Initializes the Examiner Agent.

        Args:
            agent_id (str): A unique identifier for the agent.
            gemini_client (GeminiClient): An instance of the GeminiClient for LLM interaction.
        """
        self.agent_id = agent_id
        self.gemini_client = gemini_client
        # print(f"ExaminerAgent {self.agent_id} initialized.")

    def evaluate_answer(self, question_id: str, question_text: str, candidate_answer_text: str, model_answer_text: str = None) -> dict:
        """
        Evaluates a candidate's answer to a question using the Gemini client.

        Args:
            question_id (str): The ID of the question.
            question_text (str): The text of the original question.
            candidate_answer_text (str): The candidate's submitted answer.
            model_answer_text (str, optional): A model or reference answer. Defaults to None.

        Returns:
            dict: A dictionary containing the evaluation details, including score,
                  feedback, and suggestions.
                  Example: {
                      'question_id': 'q1',
                      'evaluator_agent_id': 'e1',
                      'candidate_answer_text': '...',
                      'evaluation': {
                          'score': 90,
                          'feedback': 'Well explained...',
                          'suggestions': 'Consider adding examples...'
                      }
                  }
        """
        # print(f"ExaminerAgent {self.agent_id} received request to evaluate answer for question_id {question_id}.")
        # print(f"Question: '{question_text[:50]}...'")
        # print(f"Candidate's Answer: '{candidate_answer_text[:50]}...'")
        # if model_answer_text:
        #     print(f"Model Answer: '{model_answer_text[:50]}...'")

        # This prompt needs to be carefully designed for the LLM to understand
        # its role as an evaluator.
        evaluation_prompt_text = f"""
        You are an AI Examiner. Your task is to evaluate a candidate's answer to a question.
        
        Question:
        {question_text}
        
        Candidate's Answer:
        {candidate_answer_text}
        """

        if model_answer_text:
            evaluation_prompt_text += f"""
            
            For your reference, a Model Answer is provided below:
            {model_answer_text}
            """

        evaluation_prompt_text += f"""

        Based on the Question (and Model Answer, if provided), please:
        1. Provide a numerical score for the Candidate's Answer (e.g., out of 100).
        2. Give detailed qualitative feedback on the strengths and weaknesses of the answer.
        3. Offer specific suggestions for improvement.

        Structure your response as a JSON object with the keys "score", "feedback", and "suggestions".
        Example: {{"score": 85, "feedback": "The answer is mostly correct...", "suggestions": "Try to elaborate on..."}}
        """
        
        # The gemini_client.evaluate_text method is a placeholder.
        # In a real scenario, it would make an API call to Gemini with the crafted prompt.
        # The actual Gemini model would need to be capable of returning structured JSON
        # or the response would need parsing.
        evaluation_result = self.gemini_client.evaluate_text(
            prompt=evaluation_prompt_text, # In a real Gemini call, this might just be 'evaluation_prompt_text'
            text_to_evaluate=candidate_answer_text, # This arg might be redundant if prompt contains all
            model_answer=model_answer_text # Also potentially redundant
        )

        # print(f"ExaminerAgent {self.agent_id} received evaluation from Gemini: {evaluation_result}")

        return {
            "question_id": question_id,
            "evaluator_agent_id": self.agent_id,
            "candidate_answer_text": candidate_answer_text,
            "evaluation": evaluation_result # This comes from the GeminiClient
        }

if __name__ == '__main__':
    # Example Usage

    # If running this script directly for testing, use a dummy/placeholder client.
    try:
        from ai_exam_simulator.core.gemini_client import GeminiClient
        gemini_service = GeminiClient() # Using placeholder
    except ImportError:
        print("Falling back to DummyGeminiClient for example usage of ExaminerAgent.")
        class DummyGeminiClient: # Define a compatible dummy if GeminiClient can't be imported
            def evaluate_text(self, prompt: str, text_to_evaluate: str, model_answer: str = None, max_tokens: int = 300) -> dict:
                return {
                    "score": 75,
                    "feedback": f"Dummy feedback for: {text_to_evaluate[:30]}... based on prompt: {prompt[:30]}...",
                    "suggestions": "Dummy suggestion: Add more details."
                }
        gemini_service = DummyGeminiClient()

    examiner1 = ExaminerAgent(agent_id="examiner001", gemini_client=gemini_service)

    sample_question_id = "history_q1"
    sample_question = "What were the main causes of World War I?"
    sample_candidate_answer = "World War I was caused by the assassination of Archduke Franz Ferdinand."
    sample_model_answer = "The main causes of WWI included militarism, alliances, imperialism, and nationalism, with the assassination acting as a trigger."

    evaluation = examiner1.evaluate_answer(
        question_id=sample_question_id,
        question_text=sample_question,
        candidate_answer_text=sample_candidate_answer,
        model_answer_text=sample_model_answer
    )

    print(f"--- Example ExaminerAgent Usage ---")
    print(f"Evaluator ID: {evaluation['evaluator_agent_id']}")
    print(f"Question ID: {evaluation['question_id']}")
    print(f"Candidate Answer: {evaluation['candidate_answer_text']}")
    print(f"Score: {evaluation['evaluation']['score']}")
    print(f"Feedback: {evaluation['evaluation']['feedback']}")
    print(f"Suggestions: {evaluation['evaluation']['suggestions']}")

    evaluation_no_model = examiner1.evaluate_answer(
        question_id=sample_question_id,
        question_text=sample_question,
        candidate_answer_text=sample_candidate_answer
    )
    print(f"\n--- Evaluation without Model Answer ---")
    print(f"Score: {evaluation_no_model['evaluation']['score']}")
    print(f"Feedback: {evaluation_no_model['evaluation']['feedback']}")
