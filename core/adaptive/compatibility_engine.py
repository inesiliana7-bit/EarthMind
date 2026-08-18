import pandas as pd
from problem_categories import PROBLEM_CATEGORY

class CompatibilityEngine:

    LEVELS = {
        "Very Low": 1,
        "Low": 2,
        "Medium": 3,
        "High": 4,
        "Very High": 5
    }

    LEVEL_FIELDS = [

        "Budget_Level",

        "Development_Level",

        "Technology",

        "Infrastructure",

        "Income_Level",

        "Digitalization",

        "Healthcare",

        "Education",

        "Political_Stability"

    ]

    CATEGORY_FIELDS = [

        "Climate",

        "Religion",

        "Government",

        "Geography",

        "Economy",

        "Water",

        "Energy",

        "Agriculture",

        "Natural_Resources"

    ]

    NUMERIC_FIELDS = [

        "Population_Size",

        "Urbanization",

        "Carbon_Emissions",

        "Disaster_Risk"

    ]

    WEIGHTS = {

        "Budget_Level":10,

        "Development_Level":10,

        "Technology":12,

        "Infrastructure":12,

        "Income_Level":6,

        "Digitalization":8,

        "Healthcare":8,

        "Education":8,

        "Political_Stability":8,

        "Climate":8,

        "Religion":2,

        "Government":5,

        "Geography":4,

        "Economy":10,

        "Water":8,

        "Energy":8,

        "Agriculture":5,

        "Natural_Resources":6,

        "Population_Size":5,

        "Urbanization":4,

        "Carbon_Emissions":3,

        "Disaster_Risk":6

    }

    CLIMATE_MATRIX = {

        ("Desert", "Desert"): 100,
        ("Desert", "Mediterranean"): 75,
        ("Desert", "Temperate"): 60,
        ("Desert", "Tropical"): 40,
        ("Desert", "Polar"): 20,

        ("Mediterranean", "Mediterranean"): 100,
        ("Mediterranean", "Temperate"): 85,
        ("Mediterranean", "Tropical"): 65,
        ("Mediterranean", "Polar"): 30,

        ("Temperate", "Temperate"): 100,
        ("Temperate", "Tropical"): 70,
        ("Temperate", "Polar"): 40,

        ("Tropical", "Tropical"): 100,
        ("Tropical", "Polar"): 20,

        ("Polar", "Polar"): 100

    }

    def __init__(self):

        self.country_profiles = pd.read_csv("country_profiles.csv")

        self.problem_weights = pd.read_csv("problem_weights.csv")

    def get_problem_weights(self, problem):

        category = PROBLEM_CATEGORY.get(problem)

        if category is None:

            return self.WEIGHTS

        row = self.problem_weights[
            self.problem_weights["Category"] == category
        ]

        if row.empty:

            return self.WEIGHTS

        row = row.iloc[0].to_dict()

        row.pop("Category")

        return row

    def compare_levels(self, target_value, reference_value):

        target = self.LEVELS.get(target_value, 3)
        reference = self.LEVELS.get(reference_value, 3)

        distance = abs(target - reference)

        similarity = max(
            20,
            100 - distance * 20
        )

        return similarity

    def compare_matrix(self, matrix, target_value, reference_value):

        if (target_value, reference_value) in matrix:
            return matrix[(target_value, reference_value)]

        if (reference_value, target_value) in matrix:
            return matrix[(reference_value, target_value)]

        return 50

    def compare_numeric(self, target_value, reference_value):

        try:

            target = float(target_value)
            reference = float(reference_value)

            if max(target, reference) == 0:
                return 100

            similarity = 100 * (
                1 - abs(target - reference) / max(target, reference)
            )

            return max(20, round(similarity))

        except:

            return 50

    def calculate_compatibility(
        self,
        target,
        reference,
        problem
    ):

        weights = self.get_problem_weights(problem)

        details = {}

        for field in self.WEIGHTS.keys():

            target_value = target.get(field)
            reference_value = reference.get(field)

            if field in self.LEVEL_FIELDS:

                similarity = self.compare_levels(
                    target_value,
                    reference_value
                )

            elif field == "Climate":

                similarity = self.compare_matrix(
                    self.CLIMATE_MATRIX,
                    target_value,
                    reference_value
                )

            elif field in self.NUMERIC_FIELDS:

                similarity = self.compare_numeric(
                    target_value,
                    reference_value
                )

            elif field in self.CATEGORY_FIELDS:

                similarity = 100 if target_value == reference_value else 60

            else:

                similarity = 50

            details[field] = similarity

        weighted_sum = 0
        total_weight = 0

        for field, similarity in details.items():

            weight = weights.get(field, 5)

            weighted_sum += similarity * weight

            total_weight += weight


        strong_matches = []
        weak_matches = []

        for field, similarity in details.items():

            importance = weights.get(field, 5)

            if similarity >= 80 and importance >= 8:

                strong_matches.append({

                    "field": field,

                    "score": similarity

                })

            elif similarity <= 65 and importance >= 8:

                weak_matches.append({

                    "field": field,

                    "score": similarity

                })

        strong_matches = sorted(

            strong_matches,

            key=lambda x: x["score"],

            reverse=True

        )

        weak_matches = sorted(

            weak_matches,

            key=lambda x: x["score"]

        )
        compatibility = round(weighted_sum / total_weight)

        return {

            "score": compatibility,

            "details": details,

            "strong_matches": strong_matches,

            "weak_matches": weak_matches

        }

    def get_country_profile(self, country_name):

        result = self.country_profiles[
            self.country_profiles["Country"].str.strip().str.lower()
            ==
            country_name.strip().lower()
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()

    