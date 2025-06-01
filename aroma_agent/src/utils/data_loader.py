# aroma_agent/src/utils/data_loader.py

class DataLoader:
    def __init__(self, data_path="data/"):
        self.data_path = data_path
        print(f"DataLoader initialized. Expecting data in: {self.data_path}")

    def load_flavor_db_data(self, scent_preferences=None):
        print(f"Simulating FlavorDB load based on preferences: {scent_preferences}")
        sample_data = [
            {"molecule_name": "Limonene", "scent_profile": ["citrus", "fresh"], "found_in": ["lemons", "oranges", "lemon balm"]},
            {"molecule_name": "Linalool", "scent_profile": ["floral", "sweet", "woody"], "found_in": ["lavender", "coriander", "basil"]},
            {"molecule_name": "Pinene", "scent_profile": ["pine", "woody", "fresh"], "found_in": ["pine needles", "rosemary", "eucalyptus"]},
            {"molecule_name": "Menthone", "scent_profile": ["minty", "cool"], "found_in": ["peppermint", "spearmint"]},
            {"molecule_name": "Vanillin", "scent_profile": ["vanilla", "sweet", "balsamic"], "found_in": ["vanilla beans"]},
        ]
        if scent_preferences:
            filtered_data = [
                item for item in sample_data
                if any(pref.lower() in profile for pref in scent_preferences for profile in item["scent_profile"])
            ]
            return filtered_data if filtered_data else sample_data
        return sample_data

    def load_tcm_data(self, mood=None, purpose=None):
        print(f"Simulating TCM data load based on mood: {mood}, purpose: {purpose}")
        sample_data = [
            {"herb_name": "Gou Teng (钩藤)", "properties": ["calming", "liver wind"], "mood_association": ["irritability", "restlessness"]},
            {"herb_name": "Bo He (薄荷)", "properties": ["cooling", "refreshing", "head-clearing"], "mood_association": ["mental fatigue", "uplifting"]},
            {"herb_name": "Mei Gui Hua (玫瑰花)", "properties": ["qi circulation", "soothing"], "mood_association": ["stress", "depression", "romantic"]},
            {"herb_name": "Suan Zao Ren (酸枣仁)", "properties": ["nourishing heart", "calming spirit"], "mood_association": ["insomnia", "anxiety"]},
        ]
        if mood:
            filtered_data = [
                item for item in sample_data
                if mood.lower() in item["mood_association"]
            ]
            return filtered_data if filtered_data else sample_data
        return sample_data

    def load_user_reviews(self, plant_name=None, scent_keywords=None):
        print(f"Simulating user review load for plant: {plant_name}, keywords: {scent_keywords}")
        sample_reviews = [
            {"plant": "lavender", "rating": 5, "comment": "Very calming, helps me sleep.", "keywords": ["calming", "sleep", "floral"]},
            {"plant": "lemon balm", "rating": 4, "comment": "Refreshing citrus scent, great for focus.", "keywords": ["refreshing", "citrus", "focus"]},
            {"plant": "peppermint", "rating": 5, "comment": "Energizing and helps with headaches.", "keywords": ["energizing", "minty", "headache"]},
            {"plant": "rose", "rating": 4, "comment": "Lovely romantic fragrance, but can be strong.", "keywords": ["romantic", "floral", "strong"]},
        ]
        if plant_name:
            return [r for r in sample_reviews if r["plant"] == plant_name.lower()]
        if scent_keywords:
            filtered_reviews = [
                r for r in sample_reviews
                if any(keyword.lower() in r_keywords for keyword in scent_keywords for r_keywords in r["keywords"])
            ]
            return filtered_reviews if filtered_reviews else sample_reviews
        return sample_reviews

if __name__ == '__main__':
    loader = DataLoader()
    print("\n--- Testing FlavorDB Loader ---")
    flavor_data_citrus = loader.load_flavor_db_data(scent_preferences=["citrus"])
    print(f"FlavorDB (citrus): {flavor_data_citrus}")
    print("\n--- Testing TCM Loader ---")
    tcm_data_stress = loader.load_tcm_data(mood="stress")
    print(f"TCM (stress): {tcm_data_stress}")
    print("\n--- Testing User Review Loader ---")
    reviews_lavender = loader.load_user_reviews(plant_name="lavender")
    print(f"Reviews (lavender): {reviews_lavender}")
