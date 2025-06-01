# aroma_agent/src/utils/gemini_client.py

import time
import random

class MockGeminiClient:
    def __init__(self, api_key=None, config=None):
        self.api_key = api_key
        self.config = config if config else {}
        if self.api_key:
            print(f"MockGeminiClient initialized with API key: ...{self.api_key[-4:]}")
        else:
            print("MockGeminiClient initialized without API key (as expected for mock).")

    def generate_text(self, prompt: str, max_tokens=150, temperature=0.7) -> str:
        print(f"\n--- MockGeminiClient ---")
        prompt_preview = prompt.replace('\\n', ' ')[:70]
        print(f"Received prompt type indication (first ~70 chars): {prompt_preview}...")
        time.sleep(random.uniform(0.05, 0.15))
        prompt_lower = prompt.lower()

        if "json格式的结构化标签" in prompt_lower or "extract_intent_context" in prompt_lower:
            print("Mock Client: Detected Intent Extraction Prompt (Step 1)")
            response_dict_str = """
{
  "mood": "neutral",
  "desired_effect": "general wellness",
  "preferred_aroma": ["fresh", "clean"],
  "season": "any",
  "cultural_context": "any"
}
            """
            if "stressed" in prompt_lower or "anxious" in prompt_lower or "焦虑" in prompt_lower:
                response_dict_str = """
{
  "mood": "anxious",
  "desired_effect": "relaxing",
  "preferred_aroma": ["lavender", "chamomile", "floral"],
  "season": "any",
  "cultural_context": "western"
}
                """
            elif "happy" in prompt_lower or "joyful" in prompt_lower or "开心" in prompt_lower:
                response_dict_str = """
{
  "mood": "happy",
  "desired_effect": "uplifting",
  "preferred_aroma": ["citrus", "minty", "fresh"],
  "season": "summer",
  "cultural_context": "any"
}
                """
            elif "sad" in prompt_lower or "melancholy" in prompt_lower or "悲伤" in prompt_lower:
                response_dict_str = """
{
  "mood": "sad",
  "desired_effect": "comforting",
  "preferred_aroma": ["vanilla", "sandalwood", "warm"],
  "season": "autumn",
  "cultural_context": "any"
}
                """
            print(f"Mock Client: Returning intent: {response_dict_str.strip()}")
            return response_dict_str.strip()

        elif "候选草药组合" in prompt_lower or "generate_recommendation" in prompt_lower:
            print("Mock Client: Detected Recommendation Generation Prompt (Step 3)")
            recommendation_text = """
推荐组合:
- 柠檬草 + 薄荷: 提神醒脑, 清新空气.
- 理由: 两者都具有清新的香气, 适合需要提振精神的时刻.

推荐香氛产品:
- 一款通用的柑橘调空气清新喷雾.
"""
            if "anxious" in prompt_lower and "lavender" in prompt_lower:
                recommendation_text = """
推荐组合:
- 薰衣草 + 洋甘菊 (来自候选列表, 如果存在的话): 经典的放松组合, 有助于缓解焦虑.
- 理由: 薰衣草和洋甘菊都以其镇静和助眠的特性而闻名.

如果候选列表中没有洋甘菊, 可以考虑单独使用薰衣草.

推荐香氛产品:
- Jo Malone 薰衣草与月光花枕头喷雾
- Aesop 依兰依兰身体护理油 (带有放松的依兰花香)
"""
            elif "happy" in prompt_lower and "citrus" in prompt_lower:
                recommendation_text = """
推荐组合:
- 柠檬 + 甜橙 (来自候选列表, 如果存在的话): 充满活力的柑橘组合, 带来愉悦心情.
- 理由: 柑橘类香气通常与积极, 愉悦的情绪相关联.

推荐香氛产品:
- Fresh 西柚果香沐浴露
- Diptyque 柑橘香氛蜡烛
"""
            elif "[]" in prompt_lower or "候选草药组合:\n    []" in prompt_lower or "候选草药组合:\n    []" in prompt_lower :
                 recommendation_text = """
由于未能从您的偏好中匹配到特定的本地植物组合, 我们推荐一些广受欢迎的成品香氛:

推荐香氛产品:
- Le Labo Santal 33: 一款中性的木质调香水, 适合多种场合.
- Byredo Gypsy Water: 清新带有松针和焚香的独特气息.
"""
            print(f"Mock Client: Returning recommendation: {recommendation_text.strip()[:100]}...")
            return recommendation_text.strip()

        else:
            print("Mock Client: Detected UNKNOWN Prompt type. Returning generic message.")
            return "Mock response for unknown prompt type. Please check prompt content if this was unexpected."

if __name__ == '__main__':
    mock_client = MockGeminiClient(api_key="test_key_1234")

    print("\n--- Testing Mock Client: Intent Extraction (Stressed) ---")
    intent_prompt_stress = '用户描述如下: "I feel stressed and anxious." 请分析其意图, 返回 JSON...'
    intent_response_stress = mock_client.generate_text(intent_prompt_stress)
    print(f"Mock response for intent (stressed):\n{intent_response_stress}")

    print("\n--- Testing Mock Client: Intent Extraction (Happy) ---")
    intent_prompt_happy = '用户描述如下: "I am very happy today!" 请分析其意图, 返回 JSON...'
    intent_response_happy = mock_client.generate_text(intent_prompt_happy)
    print(f"Mock response for intent (happy):\n{intent_response_happy}")

    print("\n--- Testing Mock Client: Recommendation (Anxious, Lavender) ---")
    reco_prompt_anxious = """
    用户香气意图:
    情绪: anxious
    偏好香气: ["lavender"]
    候选草药组合:
    [{'herb_name': '薰衣草 (Lavender)', 'compound_name': 'Linalool', 'score': 1}]
    请基于用户意图...
    """
    reco_response_anxious = mock_client.generate_text(reco_prompt_anxious)
    print(f"Mock response for recommendation (anxious):\n{reco_response_anxious}")

    print("\n--- Testing Mock Client: Recommendation (Empty Candidates) ---")
    reco_prompt_empty = """
    用户香气意图:
    情绪: curious
    偏好香气: ["exotic wood"]
    候选草药组合:
    []
    请基于用户意图...
    """
    reco_response_empty = mock_client.generate_text(reco_prompt_empty)
    print(f"Mock response for recommendation (empty):\n{reco_response_empty}")
