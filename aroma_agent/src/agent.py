# aroma_agent/src/agent.py
from .utils.gemini_client import MockGeminiClient
from .utils.data_loader import DataLoader # New import

class AromaAgent:
    def __init__(self, gemini_client=None, data_loader=None, config=None):
        self.gemini_client = gemini_client if gemini_client else MockGeminiClient()
        self.data_loader = data_loader if data_loader else DataLoader() # Instantiate DataLoader
        self.config = config if config else {}

    def get_aroma_suggestion(self, mood: str, preferences: str = "") -> dict:
        print(f"Received mood: {mood}, preferences: {preferences}")

        # Placeholder for using data_loader
        # preferences_list = [p.strip() for p in preferences.split(',') if p.strip()]
        # flavor_info = self.data_loader.load_flavor_db_data(scent_preferences=preferences_list)
        # tcm_herbs = self.data_loader.load_tcm_data(mood=mood)
        # relevant_reviews = self.data_loader.load_user_reviews(scent_keywords=preferences_list)

        data_context = {
            "available_plants": [
                {"name": "Lavender", "scent_profile": ["floral", "calming"], "mood_association": ["relaxed", "sleepy"]},
                {"name": "Lemon Balm", "scent_profile": ["citrus", "fresh"], "mood_association": ["uplifting", "focused"]},
                {"name": "Peppermint", "scent_profile": ["minty", "cool"], "mood_association": ["energized", "focused"]},
                {"name": "Rosemary", "scent_profile": ["herbaceous", "woody"], "mood_association": ["focused", "memory_enhancement"]},
            ],
            "common_combinations": [
                "Lavender and Chamomile for relaxation.",
                "Lemon and Peppermint for energy."
            ]
        }
        prompt = f"""
        User input:
        Mood: {mood}
        Preferences: {preferences}

        Available data context:
        Plants: {data_context['available_plants']}
        Common Combinations: {data_context['common_combinations']}

        Task:
        Based on the user's mood and preferences, and the available data, suggest a combination of common household plants
        to create a pleasant aroma. Provide simple instructions for preparing or combining them.
        The plants should be readily available (e.g., common herbs, garden plants).
        If no suitable plant combination can be found or if the user's request is very specific and hard to match with common plants,
        suggest a type of commercial fragrance product (e.g., "a citrus-scented essential oil diffuser blend" or
        "a calming lavender room spray"). Do not invent specific product names unless they are extremely generic examples.

        Format your response as follows:
        If suggesting plants:
        Type: plant_based
        Suggestion: [Description of plant combination, e.g., "Lemon Balm and Peppermint leaves"]
        Ingredients: [List of plants, e.g., "Lemon Balm", "Peppermint"]
        Instructions: [Simple instructions, e.g., "Gently crush a few leaves of each and place them in a small dish."]
        Reasoning: [Brief explanation of why this suggestion fits the input]

        If suggesting a commercial product type:
        Type: commercial_product
        Suggestion: [Description of product type, e.g., "A refreshing citrus and mint room spray"]
        Reasoning: [Brief explanation of why this suggestion fits the input]
        """

        gemini_response_text = self.gemini_client.generate_text(prompt)

        response_parts = {}
        current_key = None
        for line in gemini_response_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                current_key = key.strip().lower()
                response_parts[current_key] = value.strip()
            elif current_key and line.strip():
                 response_parts[current_key] += " " + line.strip()

        parsed_suggestion = {
            "type": response_parts.get("type", "error"),
            "suggestion": response_parts.get("suggestion", ""),
            "ingredients": [ing.strip() for ing in response_parts.get("ingredients", "").split(',')] if response_parts.get("ingredients") else [],
            "instructions": response_parts.get("instructions", ""),
            "reasoning": response_parts.get("reasoning", "")
        }

        if parsed_suggestion["type"] == "error" or not parsed_suggestion["suggestion"]:
            if not parsed_suggestion.get("message"):
                 parsed_suggestion["message"] = "Failed to parse suggestion or no specific suggestion found."
            return parsed_suggestion
        return parsed_suggestion

if __name__ == '__main__':
    agent = AromaAgent()
    print("\n--- Test Case 1: Relaxing Mood ---")
    suggestion1 = agent.get_aroma_suggestion(mood="relaxed", preferences="I like floral scents.")
    print(suggestion1)
    print("\n--- Test Case 2: Energizing Mood ---")
    suggestion2 = agent.get_aroma_suggestion(mood="energized", preferences="Something fresh and minty, citrus")
    print(suggestion2)
    print("\n--- Test Case 3: Neutral Mood ---")
    suggestion3 = agent.get_aroma_suggestion(mood="neutral", preferences="Anything is fine.")
    print(suggestion3)
