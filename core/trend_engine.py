# ==========================================================
# EarthMind
# Global Trend Engine
# ==========================================================

class TrendEngine:

    def __init__(self):

        self.global_trends = {

            "gdp": 1.03,
            "investment": 1.05,
            "employment": 1.02,
            "inflation": 0.98,

            "air": 1.01,
            "water": 0.99,
            "carbon": 0.97,
            "forest": 1.01,

            "health": 1.02,
            "education": 1.02,
            "poverty": 0.98,
            "life": 1.02,

            "roads": 1.01,
            "internet": 1.06,
            "housing": 1.02,
            "electricity": 1.03

        }

    def factor(self, indicator):

        return self.global_trends.get(indicator, 1.0)