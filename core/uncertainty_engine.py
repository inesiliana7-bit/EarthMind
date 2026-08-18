# ==========================================================
# EarthMind
# Uncertainty Engine
# ==========================================================


class UncertaintyEngine:

    # ======================================================
    # Main Evaluation
    # ======================================================

    def evaluate(
        self,
        impact_score,
        improvement
    ):

        # --------------------------------------------------
        # Normalize impact score
        # --------------------------------------------------

        impact_score = max(
            0,
            min(
                float(impact_score),
                100
            )
        )

        improvement = max(
            0,
            float(improvement)
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        confidence = (
            70
            +
            (impact_score * 0.20)
            +
            (improvement * 0.50)
        )

        confidence = max(
            0,
            min(
                confidence,
                98
            )
        )

        # --------------------------------------------------
        # Reliability
        # --------------------------------------------------

        if confidence >= 90:

            reliability = "Very High"

        elif confidence >= 80:

            reliability = "High"

        elif confidence >= 70:

            reliability = "Moderate"

        elif confidence >= 60:

            reliability = "Low"

        else:

            reliability = "Very Low"

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        if impact_score < 30:

            risk = "High"

        elif impact_score < 50:

            risk = "Moderate"

        elif impact_score < 70:

            risk = "Low"

        else:

            risk = "Very Low"

        # --------------------------------------------------
        # Final Result
        # --------------------------------------------------

        return {

            "confidence": round(
                confidence,
                1
            ),

            "reliability": reliability,

            "risk": risk
        }