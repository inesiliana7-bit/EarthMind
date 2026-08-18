# ==========================================================
# EarthMind
# Future Simulation Engine
# ==========================================================

from core.baseline_engine import BaselineEngine
from core.adaptive_impact import AdaptiveImpact
from core.trend_engine import TrendEngine
from core.uncertainty_engine import UncertaintyEngine
from core.prediction_engine import PredictionEngine
from core.scenario_engine import ScenarioEngine


class FutureSimulationEngine:

    def __init__(self):

        self.predictor = PredictionEngine()

        self.trend = TrendEngine()

        self.uncertainty = UncertaintyEngine()

        self.scenario = ScenarioEngine()

    # ======================================================
    # Main Simulation
    # ======================================================

    def simulate(
        self,
        country_info,
        adaptive_result
    ):

        print("🔥 SIMULATION ENGINE STARTED")

        # --------------------------------------------------
        # 1. Baseline
        # --------------------------------------------------

        baseline = BaselineEngine(
            country_info
        ).build()

        print("BASELINE:")
        print(baseline)

        # --------------------------------------------------
        # 2. Scenario
        # --------------------------------------------------

        scenario = self.scenario.build(
            country_info,
            adaptive_result
        )

        # --------------------------------------------------
        # 3. Adaptive Impact
        # --------------------------------------------------

        adaptive = AdaptiveImpact(
            adaptive_result
        )

        # --------------------------------------------------
        # 4. Adaptive Impact Score
        # --------------------------------------------------

        impact_score = float(
            adaptive_result.get(
                "impact_score",
                50
            )
        )

        improvement = impact_score / 10

        # --------------------------------------------------
        # 5. Prediction
        # --------------------------------------------------

        prediction = self.predictor.build(
            baseline,
            adaptive,
            impact_score
        )

        print("================================")
        print("YEARS:")
        print(prediction["years"])

        print("SIMULATION:")
        print(prediction["simulation"])

        print("TARGETS:")
        print(prediction["targets"])
        print("================================")

        years = prediction["years"]

        predicted_values = prediction[
            "simulation"
        ]

        targets = prediction[
            "targets"
        ]

        # --------------------------------------------------
        # 6. Apply Strategic Trends
        # --------------------------------------------------

        simulation = {}

        for indicator, values in predicted_values.items():

            trend_factor = self.trend.factor(
                indicator
            )

            adjusted_values = []

            baseline_value = float(
                baseline.get(
                    indicator,
                    50
                )
            )

            for value in values:

                adjusted = (
                    baseline_value
                    +
                    (
                        float(value)
                        -
                        baseline_value
                    )
                    *
                    trend_factor
                )

                adjusted = max(
                    0,
                    min(
                        adjusted,
                        100
                    )
                )

                adjusted_values.append(
                    round(
                        adjusted,
                        2
                    )
                )

            simulation[indicator] = (
                adjusted_values
            )

        # --------------------------------------------------
        # 7. Uncertainty
        # --------------------------------------------------

        uncertainty = (
            self.uncertainty.evaluate(
                impact_score,
                improvement
            )
        )

        # --------------------------------------------------
        # 8. Explainable AI Data
        # --------------------------------------------------

        explanation = {}

        for indicator in baseline.keys():

            explanation[indicator] = {
                "adaptive_factor": round(
                    adaptive.factor(
                        indicator
                    ),
                    2
                ),
                "trend_factor": round(
                    self.trend.factor(
                        indicator
                    ),
                    2
                ),
                "baseline": round(
                    float(
                        baseline.get(
                            indicator,
                            0
                        )
                    ),
                    2
                ),
                "target": round(
                    float(
                        targets.get(
                            indicator,
                            baseline.get(
                                indicator,
                                0
                            )
                        )
                    ),
                    2
                )
            }

        # --------------------------------------------------
        # 9. Final Result
        # --------------------------------------------------

        return {

            "years": years,

            "baseline": baseline,

            "simulation": simulation,

            "targets": targets,

            "confidence": uncertainty[
                "confidence"
            ],

            "reliability": uncertainty[
                "reliability"
            ],

            "risk": uncertainty[
                "risk"
            ],

            "explanation": explanation

        }