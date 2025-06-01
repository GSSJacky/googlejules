import argparse
import pandas as pd
import os
from .utils.gemini_client import MockGeminiClient # Added import

# Path settings
BASE_DIR = os.path.dirname(__file__)
FLAVOR_PATH = os.path.join(BASE_DIR, "compounds_summary.csv")
HERB_PATH = os.path.join(BASE_DIR, "herb_flavordb_mapping.csv")

# Load data
flavor_df = pd.read_csv(FLAVOR_PATH)
herb_df = pd.read_csv(HERB_PATH)

# Initialize Gemini Model
gemini = MockGeminiClient() # Instantiated MockGeminiClient

# Step 1: Parse user input to structured context
def extract_intent_context(user_input: str) -> dict:
    prompt = f"""
    用户描述如下："{user_input}"
    请分析其意图，返回 JSON 格式的结构化标签，包括：
    - mood: 情绪状态
    - desired_effect: 希望达到的效果
    - preferred_aroma: 最多 3 个英文关键词（如 floral, woody, minty）
    - season: 当前季节（如 spring, summer）
    - cultural_context: 可选文化背景（如 east_asian, western）
    """
    text_response = gemini.generate_text(prompt) # Adapted API call
    try:
        context_str = text_response.strip()
        if context_str.startswith('{') and context_str.endswith('}'):
            context = eval(context_str) # Using eval as per original code for consistency
            return context
        else:
            # Fallback logic if the response is not a direct JSON string
            print(f"Warning: Gemini response for intent extraction was not a direct JSON: {context_str}")
            # Heuristic based on keywords in user_input for mock context generation
            user_input_lower = user_input.lower()
            if "悲伤" in user_input_lower or "sad" in user_input_lower:
                return {"mood": "sad", "desired_effect": "comfort", "preferred_aroma": ["vanilla", "sweet"], "season": "any", "cultural_context": "any"}
            elif "浪漫" in user_input_lower or "romantic" in user_input_lower:
                return {"mood": "romantic", "desired_effect": "ambiance", "preferred_aroma": ["rose", "jasmine"], "season": "any", "cultural_context": "any"}
            elif "放松" in user_input_lower or "relax" in user_input_lower or "calm" in user_input_lower:
                return {"mood": "relaxed", "desired_effect": "calm", "preferred_aroma": ["lavender", "chamomile"], "season": "any", "cultural_context": "any"}
            elif "提神" in user_input_lower or "energ" in user_input_lower or "focus" in user_input_lower:
                return {"mood": "energized", "desired_effect": "focus", "preferred_aroma": ["citrus", "mint"], "season": "any", "cultural_context": "any"}
            else:
                return {"mood": "neutral", "desired_effect": "pleasant scent", "preferred_aroma": ["fresh", "clean"], "season": "any", "cultural_context": "any"}
    except Exception as e:
        print(f"Error processing Gemini response for intent: {e}")
        print(f"Problematic response for intent: {text_response}")
        return {"mood": "error", "desired_effect": "error", "preferred_aroma": [], "season": "any", "cultural_context": "any"}


# Step 2: Local aroma molecule and herb matching + scoring
def search_candidates(aroma_tags):
    if not aroma_tags or not isinstance(aroma_tags, list) or not all(isinstance(tag, str) for tag in aroma_tags):
        print(f"Warning: Invalid aroma_tags: {aroma_tags}. Returning empty list.")
        return []

    # Ensure 'flavor_profile' is string and handle NaN
    flavor_df['flavor_profile'] = flavor_df['flavor_profile'].fillna('')

    matched_mols = flavor_df[flavor_df['flavor_profile'].apply(
        lambda x: any(tag.lower() in x.lower() for tag in aroma_tags))]

    # Ensure 'pubchem_id' in herb_df is of a type that can be compared with matched_mols['pubchem_id']
    # If pubchem_id can be NaN, ensure it's handled, e.g. by dropping rows or converting types.
    # For this example, assume pubchem_id are compatible types (e.g. int or string consistently)
    # and that missing values that would break 'isin' are handled if necessary.

    # Convert pubchem_id columns to a common type, e.g., string, to ensure 'isin' works robustly
    herb_df['pubchem_id'] = herb_df['pubchem_id'].astype(str)
    matched_mols['pubchem_id'] = matched_mols['pubchem_id'].astype(str)

    candidates = herb_df[herb_df['pubchem_id'].isin(matched_mols['pubchem_id'].unique())] # Added .unique() for efficiency

    if candidates.empty:
        return []

    # Group by herb and compound_name, then count occurrences for score.
    # This assumes 'compound_name' is the name of the molecule in the herb.
    scored = candidates.groupby(['herb_name', 'compound_name']).size().reset_index(name='score') # Changed 'herb' to 'herb_name'
    return scored.sort_values(by='score', ascending=False).to_dict(orient='records')

# Step 3: Gemini judges candidate combinations and generates suggestions
def generate_recommendation(context: dict, candidates: list) -> str:
    prompt = f"""
    用户香气意图：
    情绪: {context.get('mood')}
    目标: {context.get('desired_effect')}
    偏好香气: {context.get('preferred_aroma')}
    季节: {context.get('season')}
    文化背景: {context.get('cultural_context')}

    候选草药组合（草药名 - 分子名 - 评分）：
    {str(candidates[:10])} # Ensure candidates list is converted to string for the prompt

    请基于用户意图，判断最合适的香气配方（最多3种草药），并给出理由。
    如果没有合适植物，请推荐现成的香氛商品替代。
    用自然语言简洁输出。
    """
    text_response = gemini.generate_text(prompt) # Adapted API call
    return text_response.strip() # Adapted API call


# Main Agent Invocation Flow
def run_agent_advanced(user_input: str):
    print("\n🧠 正在理解用户意图……")
    context = extract_intent_context(user_input)
    if not context:
        print("⚠️ 无法解析用户输入。")
        return
    print("🎯 结构化意图：", context)

    print("\n🔍 匹配草药成分中……")
    # Ensure preferred_aroma is a list of strings
    preferred_aromas = context.get("preferred_aroma", [])
    if isinstance(preferred_aromas, str):
        preferred_aromas = [s.strip() for s in preferred_aromas.split(',') if s.strip()]

    candidates = search_candidates(preferred_aromas) # Use the processed list

    if not candidates:
        # If no candidates, directly call Gemini for a general recommendation or fallback
        print("❌ 未直接匹配到相关植物。尝试通用推荐。")
        # Fallback: Call generate_recommendation with empty candidates.
        # Gemini will rely solely on context.
        suggestion = generate_recommendation(context, [])
    else:
        print(f"🌿 发现 {len(candidates)} 个潜在候选：{[(c['herb_name'], c['compound_name']) for c in candidates[:5]]}...") # Displaying first 5
        print("\n🤖 Gemini 正在生成推荐配方……")
        suggestion = generate_recommendation(context, candidates)

    print("\n✅ 推荐输出：\n")
    print(suggestion)

# CLI Interface Entry
def main():
    parser = argparse.ArgumentParser(description="高级香气推荐 Agent (多阶段 Gemini)")
    parser.add_argument("--query", type=str, required=True, help="用户的自然语言香气需求")
    args = parser.parse_args()
    run_agent_advanced(args.query)

if __name__ == "__main__":
    main()
