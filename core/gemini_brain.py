import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiBrain:

    def build_prompt(
        self,
        country,
        news,
        nasa,
        available_problems
    ):

        return f"""
You are EarthMind AI, an advanced global environmental intelligence system.

Country:
{country}

News:
{news}
NASA Events:
{nasa}

Available Problems:
{available_problems}

Your tasks:

1. Analyze ALL national problems that appear in the news.

2. Compare every detected problem.

3. Score every problem according to:
- Urgency
- Human impact
- Economic impact
- Environmental impact
- National importance
- Frequency in the news.

4. Rank all detected problems from highest score to lowest score.

5. Select ONLY the highest ranked problem.

6. Never confuse the root cause with the current crisis.

Example:

Climate Change
↓
Wildfires

Detected Problem:
Wildfires

Root Cause:
Climate Change

7. Distinguish carefully between geopolitical tensions and active armed conflict.

Use "Border Tensions" when the evidence shows:
- geopolitical rivalry
- diplomatic tensions
- border disputes
- heightened security concerns
- threats or warnings
- risk of escalation
- regional instability
BUT there is NO confirmed active armed fighting.

Use "Armed Conflict" ONLY when the evidence explicitly confirms:
- active armed fighting
- military hostilities
- armed attacks
- ongoing combat
- confirmed military confrontation.

IMPORTANT:
Do NOT classify a situation as "Border Conflict" or "Armed Conflict"
merely because there is geopolitical rivalry or a possibility of escalation.

For the current evidence, if there is tension without active fighting,
the correct classification is:

primary_problem: "Border Tensions"
primary_problem_ar: "التوترات الحدودية"

8. Return the primary detected problem as:

primary_problem

9. Return all other important detected problems as:

secondary_problems

10. Estimate confidence (0–100).

11. Explain why this confidence score was assigned.

Return:

confidence_reason

12. Estimate how much the news supports this conclusion.

Return:

news_coverage

13. Estimate how much NASA scientific observations support this conclusion.

Return:

scientific_support

IMPORTANT:

If NASA Events are empty or no NASA/scientific observations are provided,
scientific_support MUST be 0.

Never estimate scientific support from news sources.

Only NASA/scientific observations may contribute to scientific_support.

14. Identify the affected sectors.

Choose only from:

Environment
Economy
Health
Agriculture
Infrastructure
Energy
Water
Security
Society

Return:

impact_dimensions

15. Predict future consequences if the problem is ignored.

16. Provide one strategic recommendation.

17. Evaluate the quality of the available evidence.

Possible values:

Excellent
Good
Limited
Insufficient

Return:

data_quality

Return ONLY a valid JSON object.

Example:

{{
"primary_problem": "Wildfires",
"primary_problem_ar": "حرائق الغابات",

"secondary_problems": [
    "Heat Waves",
    "Water Scarcity"
],

"confidence": 94,

"confidence_reason": "Multiple trusted news sources strongly support this conclusion.",
"confidence_reason_ar": "تدعم عدة مصادر إخبارية موثوقة هذا الاستنتاج بقوة.",

"summary": "...",
"summary_ar": "...",

"why_selected": "...",
"why_selected_ar": "...",

"root_cause": "Climate Change",
"root_cause_ar": "تغير المناخ",

"risk_level": "High",
"risk_level_ar": "مرتفع",

"news_coverage": 78,
"scientific_support": 86,

"impact_dimensions": [
    "Environment",
    "Economy",
    "Health"
],

"impact_dimensions_ar": [
    "البيئة",
    "الاقتصاد",
    "الصحة"
],

"future_consequences": "...",
"future_consequences_ar": "...",

"recommendation": "...",
"recommendation_ar": "...",

"key_findings": [
    "...",
    "..."
],

"key_findings_ar": [
    "...",
    "..."
],

"data_quality": "Excellent"
}}

Return ONLY a valid JSON object with these keys:

primary_problem
secondary_problems
problem_ranking
confidence
confidence_reason
summary
why_selected
root_cause
risk_level
news_coverage
scientific_support
impact_dimensions
future_consequences
recommendation
key_findings
data_quality

IMPORTANT LANGUAGE REQUIREMENT:

For every textual field, return both English and Arabic versions.

Use these exact additional keys:

primary_problem_ar
confidence_reason_ar
summary_ar
why_selected_ar
root_cause_ar
risk_level_ar
impact_dimensions_ar
future_consequences_ar
recommendation_ar
key_findings_ar

The Arabic versions must be natural Modern Standard Arabic and must preserve the exact meaning of the English versions.

Do NOT translate scientific names, country names, or technical terminology incorrectly.

For example:

"primary_problem": "Wildfires",
"primary_problem_ar": "حرائق الغابات"

"root_cause": "Climate Change",
"root_cause_ar": "تغير المناخ"

"risk_level": "High",
"risk_level_ar": "مرتفع"

IMPORTANT OUTPUT FORMAT:

Return ONLY JSON.

Do NOT return HTML.
Do NOT return Markdown.
Do NOT return <div>, <ul>, <li>, <br>, CSS, or any UI code.

The values of:
adaptive_solution_en
adaptive_solution_ar

must contain plain text only.

The values of:
adaptation_points_en
adaptation_points_ar

must contain plain text list items only.
...
"""

    def analyze(self, country, news, nasa, available_problems):

        print("ENTERED GEMINI")

        print(
            "Gemini API Loaded:",
            bool(os.getenv("GEMINI_API_KEY"))
        )

        prompt = self.build_prompt(
            country,
            news,
            nasa,
            available_problems
        )

        print("SENDING TO GEMINI...")
        print("Using model: gemini-2.5-flash")

        import time

        response = None

        # ==============================
        # GEMINI REQUEST WITH RETRIES
        # ==============================

        try:

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    break

                except Exception as e:

                    print(
                        f"Attempt {attempt + 1} failed:",
                        e
                    )

                    if attempt == 2:
                        raise

                    time.sleep(3)

            # ==============================
            # CHECK RESPONSE
            # ==============================

            if response is None:

                return {
                    "primary_problem": "Unknown problem",
                    "secondary_problems": [],
                    "problem_ranking": [],
                    "confidence": 0,
                    "confidence_reason": "",
                    "summary": "Gemini unavailable.",
                    "why_selected": "",
                    "root_cause": "",
                    "risk_level": "Unknown",
                    "news_coverage": 0,
                    "scientific_support": 0,
                    "impact_dimensions": [],
                    "future_consequences": "",
                    "recommendation": "",
                    "key_findings": [],
                    "data_quality": "Insufficient"
                }

            # ==============================
            # RAW RESPONSE
            # ==============================

            text = response.text

            print("=" * 60)
            print("RAW GEMINI RESPONSE:")
            print(text)
            print("=" * 60)

            # ==============================
            # CLEAN JSON
            # ==============================

            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            # ==============================
            # VALIDATE JSON FORMAT
            # ==============================

            if not text.startswith("{"):

                print("Gemini did not return JSON!")

                return {
                    "primary_problem": "Unknown problem",
                    "secondary_problems": [],
                    "problem_ranking": [],
                    "confidence": 0,
                    "confidence_reason": "",
                    "summary": "Invalid Gemini response format.",
                    "why_selected": "",
                    "root_cause": "",
                    "risk_level": "Unknown",
                    "news_coverage": 0,
                    "scientific_support": 0,
                    "impact_dimensions": [],
                    "future_consequences": "",
                    "recommendation": "",
                    "key_findings": [],
                    "data_quality": "Insufficient"
                }

            # ==============================
            # PARSE JSON
            # ==============================

            result = json.loads(text)

            # ==============================
            # SAFETY DEFAULTS
            # ==============================

            result.setdefault(
                "primary_problem",
                "Unknown problem"
            )

            result.setdefault(
                "secondary_problems",
                []
            )

            result.setdefault(
                "problem_ranking",
                []
            )

            result.setdefault(
                "confidence",
                0
            )

            result.setdefault(
                "confidence_reason",
                ""
            )

            result.setdefault(
                "summary",
                ""
            )

            result.setdefault(
                "why_selected",
                ""
            )

            result.setdefault(
                "root_cause",
                ""
            )

            result.setdefault(
                "risk_level",
                "Unknown"
            )

            result.setdefault(
                "news_coverage",
                0
            )

            result.setdefault(
                "scientific_support",
                0
            )

            result.setdefault(
                "impact_dimensions",
                []
            )

            result.setdefault(
                "future_consequences",
                ""
            )

            result.setdefault(
                "recommendation",
                ""
            )

            result.setdefault(
                "key_findings",
                []
            )

            result.setdefault(
                "data_quality",
                "Insufficient"
            )

            result.setdefault("primary_problem_ar", "غير معروف")
            result.setdefault("confidence_reason_ar", "")
            result.setdefault("summary_ar", "")
            result.setdefault("why_selected_ar", "")
            result.setdefault("root_cause_ar", "")
            result.setdefault("risk_level_ar", "غير معروف")
            result.setdefault("impact_dimensions_ar", [])
            result.setdefault("future_consequences_ar", "")
            result.setdefault("recommendation_ar", "")
            result.setdefault("key_findings_ar", [])

            return result

        # ==============================
        #GEMINI ERRORS
        # ==============================

        except Exception as e:

            print("=" * 60)
            print("GEMINI ERROR:")
            print(e)
            print("=" * 60)

            if "503" in str(e):

                return {
                    "primary_problem": "SERVICE_BUSY",
                    "secondary_problems": [],
                    "problem_ranking": [],
                    "confidence": 0,
                    "confidence_reason": "",
                    "summary": "Gemini servers are busy.",
                    "why_selected": "",
                    "root_cause": "",
                    "risk_level": "Unknown",
                    "news_coverage": 0,
                    "scientific_support": 0,
                    "impact_dimensions": [],
                    "future_consequences": "",
                    "recommendation": "",
                    "key_findings": [],
                    "data_quality": "Insufficient"
                }

            elif "429" in str(e):

                return {
                    "primary_problem": "QUOTA_EXCEEDED",
                    "secondary_problems": [],
                    "problem_ranking": [],
                    "confidence": 0,
                    "confidence_reason": "",
                    "summary": "Gemini quota exceeded.",
                    "why_selected": "",
                    "root_cause": "",
                    "risk_level": "Unknown",
                    "news_coverage": 0,
                    "scientific_support": 0,
                    "impact_dimensions": [],
                    "future_consequences": "",
                    "recommendation": "",
                    "key_findings": [],
                    "data_quality": "Insufficient"
                }

            else:

                return {
                    "primary_problem": "Unknown problem",
                    "secondary_problems": [],
                    "problem_ranking": [],
                    "confidence": 0,
                    "confidence_reason": "",
                    "summary": "Gemini unavailable.",
                    "why_selected": "",
                    "root_cause": "",
                    "risk_level": "Unknown",
                    "news_coverage": 0,
                    "scientific_support": 0,
                    "impact_dimensions": [],
                    "future_consequences": "",
                    "recommendation": "",
                    "key_findings": [],
                    "data_quality": "Insufficient"
                }