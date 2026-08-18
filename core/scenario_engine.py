# ==========================================================
# EarthMind
# Scenario Engine
# ==========================================================


class ScenarioEngine:

    def build(
        self,
        country,
        adaptive_result
    ):

        success = float(
            adaptive_result.get(
                "estimated_success",
                70
            )
        )

        development = str(
            country["Development_Level"]
        ).lower()

        stability = str(
            country["Political_Stability"]
        ).lower()

        score = success

        if "high" in development:
            score += 8

        elif "medium" in development:
            score += 3

        if "high" in stability:
            score += 8

        elif "medium" in stability:
            score += 3

        # =========================

        if score >= 90:

            return {

                "scenario": "Optimistic",

                "speed": 1.25,

                "noise": 0.20,

                "shock_probability": 0.05

            }

        elif score >= 75:

            return {

                "scenario": "Normal",

                "speed": 1.00,

                "noise": 0.40,

                "shock_probability": 0.10

            }

        elif score >= 60:

            return {

                "scenario": "Conservative",

                "speed": 0.80,

                "noise": 0.60,

                "shock_probability": 0.20

            }

        else:

            return {

                "scenario": "Crisis",

                "speed": 0.55,

                "noise": 0.90,

                "shock_probability": 0.40

            }