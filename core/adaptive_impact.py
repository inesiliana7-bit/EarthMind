# ==========================================================
# EarthMind
# Adaptive Impact Engine
# ==========================================================

class AdaptiveImpact:

    def __init__(self, adaptive_result):

        self.result = adaptive_result

    def factor(self, indicator):

        text = str(self.result).lower()

        factor = 1.0

        keywords = {

            "gdp": [
                "economy",
                "investment",
                "industry",
                "trade",
                "finance"
            ],

            "investment": [
                "investment",
                "finance",
                "industry"
            ],

            "employment": [
                "employment",
                "jobs",
                "industry"
            ],

            "inflation": [
                "inflation",
                "finance"
            ],

            "air": [
                "air",
                "pollution",
                "environment"
            ],

            "water": [
                "water",
                "irrigation",
                "desalination"
            ],

            "forest": [
                "forest",
                "green",
                "trees"
            ],

            "carbon": [
                "carbon",
                "climate",
                "emissions"
            ],

            "education": [
                "education",
                "school",
                "university"
            ],

            "health": [
                "health",
                "hospital",
                "medical"
            ],

            "poverty": [
                "poverty",
                "income"
            ],

            "life": [
                "quality",
                "life"
            ],

            "roads": [
                "road",
                "transport"
            ],

            "internet": [
                "digital",
                "internet",
                "technology"
            ],

            "housing": [
                "housing",
                "urban"
            ],

            "electricity": [
                "energy",
                "electricity",
                "power"
            ]

        }

        for word in keywords.get(indicator, []):

            if word in text:

                factor += 0.18

        return min(factor, 1.8)