# ==========================================================
# EarthMind
# Prediction Engine
# ==========================================================

import math
import random
from core.dependency_engine import DependencyEngine
from core.economic_dynamics import EconomicDynamics
from core.shock_engine import ShockEngine

class PredictionEngine:

    def __init__(self):

        self.start_year = 2026
        self.end_year = 2035

        self.years = list(
            range(
                self.start_year,
                self.end_year + 1
            )
        )

        self.metric_profiles = {

            "gdp":         {"speed": 5.5, "curve": "growth"},
            "employment":  {"speed": 4.5, "curve": "growth"},
            "investment":  {"speed": 6.0, "curve": "growth"},

            "health":      {"speed": 4.0, "curve": "growth"},
            "education":   {"speed": 3.5, "curve": "growth"},
            "life":        {"speed": 4.2, "curve": "growth"},

            "roads":       {"speed": 2.8, "curve": "growth"},
            "housing":     {"speed": 3.0, "curve": "growth"},
            "internet":    {"speed": 7.0, "curve": "growth"},
            "electricity": {"speed": 4.5, "curve": "growth"},

            "air":         {"speed": 3.0, "curve": "growth"},
            "water":       {"speed": 2.5, "curve": "growth"},
            "forest":      {"speed": 2.2, "curve": "growth"},

            "inflation":   {"speed": 5.0, "curve": "decline"},
            "carbon":      {"speed": 2.5, "curve": "decline"},
            "poverty":     {"speed": 4.0, "curve": "decline"}
        }

        self.dependencies = DependencyEngine()

        self.dynamics = EconomicDynamics()

        self.shocks = ShockEngine(seed=42)

    
    # ======================================================
    # Build Targets
    # ======================================================

    def build_targets(
        self,
        baseline,
        adaptive_impact,
        impact_score
    ):

        targets = {}

        # ======================================================
        # 1. Normalize impact
        # ======================================================

        impact = max(
            0.0,
            min(
                float(impact_score) / 100,
                1.0
            )
        )

        # ======================================================
        # 2. Positive indicators
        # ======================================================

        positive_limits = {

            "gdp": 20,
            "employment": 15,
            "investment": 25,

            "air": 15,
            "water": 18,
            "forest": 12,

            "health": 15,
            "education": 14,
            "life": 12,

            "roads": 12,
            "electricity": 14,
            "internet": 25,
            "housing": 12
        }

        positive = list(
            positive_limits.keys()
        )

        # ======================================================
        # 3. Calculate positive targets
        # ======================================================

        for metric in positive:

            current = float(
                baseline.get(
                    metric,
                    50
                )
            )

            factor = adaptive_impact.factor(
                metric
            )

            # ----------------------------------------------
            # Remaining potential
            # ----------------------------------------------

            remaining = 100 - current

            # ----------------------------------------------
            # Scenario effectiveness
            # ----------------------------------------------

            effectiveness = (
                0.20
                +
                0.55 * impact
            )

            # ----------------------------------------------
            # Adaptive effect
            # ----------------------------------------------

            adaptive_effect = (
                1
                +
                (factor - 1)
                * 0.60
            )

            # ----------------------------------------------
            # Raw improvement
            # ----------------------------------------------

            gain = (
                remaining
                * effectiveness
                * adaptive_effect
                * 0.30
            )

            # ----------------------------------------------
            # Indicator-specific realistic ceiling
            # ----------------------------------------------

            gain = min(
                gain,
                positive_limits[metric]
            )

            target = current + gain

            targets[metric] = round(
                max(
                    0,
                    min(
                        target,
                        100
                    )
                ),
                2
            )

        # ======================================================
        # 4. Negative indicators
        # ======================================================

        negative_limits = {

            "inflation": 12,
            "carbon": 18,
            "poverty": 18
        }

        negative = list(
            negative_limits.keys()
        )

        # ======================================================
        # 5. Calculate negative targets
        # ======================================================

        for metric in negative:

            current = float(
                baseline.get(
                    metric,
                    50
                )
            )

            factor = adaptive_impact.factor(
                metric
            )

            # ----------------------------------------------
            # Scenario effectiveness
            # ----------------------------------------------

            effectiveness = (
                0.15
                +
                0.50 * impact
            )

            adaptive_effect = (
                1
                +
                (factor - 1)
                * 0.60
            )

            # ----------------------------------------------
            # Possible reduction
            # ----------------------------------------------

            reduction = (
                current
                * effectiveness
                * adaptive_effect
                * 0.30
            )

            reduction = min(
                reduction,
                negative_limits[metric]
            )

            target = current - reduction

            targets[metric] = round(
                max(
                    0,
                    min(
                        target,
                        100
                    )
                ),
                2
            )

        return targets


    # ======================================================
    # Build Prediction
    # ======================================================

    def build(
        self,
        baseline,
        adaptive_impact,
        impact_score
    ):

        simulation = {}

        shocks_history = {}

        # ==========================================
        # 1. Build strategic targets
        # ==========================================

        targets = self.build_targets(
            baseline,
            adaptive_impact,
            impact_score
        )

        # ==========================================
        # 2. Current state starts from baseline
        # ==========================================

        state = baseline.copy()

        # ==========================================
        # 3. Prepare simulation storage
        # ==========================================

        for metric in baseline:

            simulation[metric] = []

        # ==========================================
        # 4. Year-by-year simulation
        # ==========================================

        for year_index, year in enumerate(self.years):

            # --------------------------------------
            # Record current state
            # --------------------------------------

            for metric in state:

                simulation[metric].append(
                    round(
                        state[metric],
                        2
                    )
                )

            # --------------------------------------
            # Stop after 2035
            # --------------------------------------

            if year_index == len(self.years) - 1:

                break

            # ======================================
            # 5. Start next year from current state
            # ======================================

            next_state = state.copy()

            # ======================================
            # 6. Realistic annual progression
            # ======================================

            base_speeds = {

                "gdp": 0.08,
                "employment": 0.07,
                "investment": 0.10,

                "air": 0.06,
                "water": 0.05,
                "forest": 0.04,

                "health": 0.06,
                "education": 0.05,
                "life": 0.045,

                "roads": 0.04,
                "electricity": 0.06,
                "internet": 0.12,
                "housing": 0.04,

                "inflation": 0.07,
                "carbon": 0.05,
                "poverty": 0.06
            }

            for metric in next_state:

                current = float(
                    state[metric]
                )

                target = float(
                    targets.get(
                        metric,
                        current
                    )
                )

                remaining = target - current

                speed = base_speeds.get(
                    metric,
                    0.05
                )

                # --------------------------------------
                # Time-dependent acceleration
                # --------------------------------------

                year_progress = (
                    year_index /
                    (len(self.years) - 1)
                )

                # الإصلاحات تحتاج وقتًا حتى يظهر أثرها
                time_factor = (
                    0.70
                    +
                    0.60 * year_progress
                )

                # --------------------------------------
                # Diminishing returns
                # --------------------------------------

                distance_factor = min(
                    abs(remaining) / 25,
                    1.0
                )

                # --------------------------------------
                # Annual change
                # --------------------------------------

                change = (
                    remaining
                    * speed
                    * time_factor
                    * (
                        0.65
                        +
                        0.35 * distance_factor
                    )
                )

                next_state[metric] = (
                    current + change
                )

            # ======================================
            # 7. Economic dynamics
            # ======================================

            next_state = self.dynamics.next_year(
                next_state
            )

            # ======================================
            # 8. Cross-sector dependencies
            # ======================================

            next_state = self.dependencies.apply(
                next_state
            )

            # ======================================
            # 9. External shocks
            # ======================================

            next_state, triggered_shocks = self.shocks.apply(
                next_state
            )

            shocks_history[year + 1] = (
                triggered_shocks
            )

            # ======================================
            # 10. Safety bounds
            # ======================================

            for metric in next_state:

                next_state[metric] = max(
                    0,
                    min(
                        next_state[metric],
                        100
                    )
                )

            # ======================================
            # 11. Move to next year
            # ======================================

            state = next_state

        # ==========================================
        # Final result
        # ==========================================

        return {

            "years": self.years,

            "baseline": baseline,

            "targets": targets,

            "simulation": simulation,

            "shocks": shocks_history

        }