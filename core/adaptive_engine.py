import json
import time
from google import genai
from core.adaptive.compatibility_engine import CompatibilityEngine
from core.adaptive.adaptation_explainer import AdaptationExplainer

class AdaptiveEngine:

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.compatibility = CompatibilityEngine()
        self.explainer = AdaptationExplainer()

    def adapt_solution(
        self,
        country_info,
        analysis,
        reference_solution
    ):
        
        if reference_solution is None:
            return {
                "adaptive_solution": None,
                "estimated_success": 0,
                "estimated_duration": 0,
                "budget_level": country_info.get(
                    "Budget_Level",
                    "Unknown"
                ),
                "status": "NO_REFERENCE_SOLUTION"
            }

        problem = analysis.get(
            "primary_problem",
            analysis.get("problem", "Unknown")
        )

        reference_country = reference_solution.get("Country_EN")

        reference_solution_name = reference_solution.get("Solution_EN")

        reference_success = reference_solution.get("Success_Rate")

        reference_duration = reference_solution.get("Implementation_Years")

        sector = reference_solution.get("Sector_EN")

        
        country_profile = f"""
Country: {country_info.get("country","")}

Population: {country_info.get("population","Unknown")}

GDP: {country_info.get("gdp","Unknown")}

Climate: {country_info.get("climate","Unknown")}

Geography: {country_info.get("geography","Unknown")}

Economy: {country_info.get("economy","Unknown")}

Religion: {country_info.get("religion","Unknown")}

Infrastructure: {country_info.get("infrastructure","Unknown")}
"""

        adaptation_data = {
            "target_country": country_info,
            "reference_country": {
                "country": reference_country,
                "solution": reference_solution_name,
                "success_rate": reference_success,
                "duration": reference_duration,
                "sector": sector
            },
            "adaptation_points": [],
            "problem": problem
        }

        print("=" * 50)
        print("Reference country:", reference_country)
        print("Type:", type(reference_country))
        print("=" * 50)
        reference = self.compatibility.get_country_profile(
            reference_country
        )
        print(reference)

        compatibility = self.compatibility.calculate_compatibility(
            country_info,
            reference,
            problem
        )

        adaptation_explanation = {
            "compatibility_score": compatibility["score"],
            "strengths": [],
            "limitations": [],
            "adaptation_points": []
        }

        strong_matches = compatibility["strong_matches"]

        weak_matches = compatibility["weak_matches"]

        compatibility_details = compatibility["details"]

        estimated_success = self.calculate_success_rate(
            reference_success,
            compatibility["score"]
        )

        estimated_duration = self.calculate_duration(
            reference_duration,
            country_info
        )

        reference_country = {
            k: (
                int(v) if hasattr(v, "item") else v
            )
            for k, v in adaptation_data["reference_country"].items()
        }


        prompt = f"""

You are EarthMind Adaptive Intelligence.

Your task is to ADAPT an already successful solution.

DO NOT invent another solution.

Write ONE executive summary only.

Maximum 80 words.

Professional report style.

No repetition.

No bullet points.

No introduction.

No conclusion.

Focus only on the adaptations.

Target country profile:

{json.dumps(country_info, indent=4)}

Reference solution:

{json.dumps(
    reference_country,
    indent=4
)}

Problem:

{problem}

Compatibility Analysis

Overall Compatibility:

{compatibility["score"]}%

Strong Similarities:

{json.dumps(strong_matches, indent=4)}

Major Differences:

{json.dumps(weak_matches, indent=4)}

Detailed Comparison:

{json.dumps(compatibility_details, indent=4)}

Rules:

- Keep the same core strategy.
- Modify implementation only according to:
    • economy
    • budget
    • technology
    • education
    • infrastructure
    • population
    • climate
    • geography
    • religion
    • government
Use the compatibility analysis to decide exactly which parts of the reference solution should remain unchanged and which parts must be adapted.

Language requirements:

- Every textual result must be provided in BOTH English and Arabic.
- Never return an English-only solution.
- adaptive_solution_en = complete solution in English.
- adaptive_solution_ar = complete solution in Arabic.
- adaptation_points_en = concise adaptation points in English.
- adaptation_points_ar = the same adaptation points in Arabic.

Adaptation Points Rules

- Return EXACTLY 4 adaptation points.
- Each point must contain only:
    - "what"
    - "why"
- Each "what" must be ONE concise sentence.
- Each "why" must be ONE concise sentence.
- Maximum 15 words for "what".
- Maximum 20 words for "why".
- Focus only on the most important adaptations.
- Avoid repetition.
- Avoid long explanations.
- Do NOT write paragraphs.
- Do NOT use bullet points.
- Do NOT return HTML.
- Return ONLY valid JSON.

Do NOT expose internal compatibility calculations.
Do NOT write phrases such as "60% compatibility" inside adaptation points.

Keep each adaptation point concise.

Return ONLY valid JSON.

{{
    "adaptive_solution_en": "",
    "adaptive_solution_ar": "",
    "estimated_success": 0,
    "estimated_duration": 0,
    "budget_level_en": "",
    "budget_level_ar": "",
    "adaptation_points_en": [
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }}
    ],

    "adaptation_points_ar": [
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }},
        {{
            "what": "",
            "why": ""
        }}
    ]
}}
"""
        response = None
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                break
            except Exception as e:
                error_text = str(e)

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                    if attempt < max_attempts - 1:
                        wait_seconds = 8 * (attempt + 1)
                        print(f"Gemini quota reached. Retrying in {wait_seconds}s...")
                        time.sleep(wait_seconds)
                        continue

                    print("Gemini quota still unavailable after retries.")
                    return {
                        "adaptive_solution_en": reference_solution_name,
                        "adaptive_solution_ar": "الحل المتكيف غير متوفر حاليًا.",
                        "estimated_success": estimated_success,
                        "estimated_duration": estimated_duration,
                        "budget_level_en": country_info.get("Budget_Level", "Unknown"),
                        "budget_level_ar": "غير متوفر حاليًا",
                        "adaptation_points_en": [
                            {"what": "Keep the reference solution's core strategy.",
                             "why": "The reference solution has already demonstrated successful implementation elsewhere."},
                            {"what": "Adapt implementation to local infrastructure.",
                             "why": "Local infrastructure determines practical deployment requirements."},
                            {"what": "Adjust implementation to local budget constraints.",
                             "why": "Available resources affect deployment scale and timing."},
                            {"what": "Adapt delivery to local institutional capacity.",
                             "why": "Implementation depends on local technical and administrative capacity."}
                        ],
                        "adaptation_points_ar": [
                            {"what": "الحفاظ على الاستراتيجية الأساسية للحل المرجعي.",
                             "why": "الحل المرجعي أثبت نجاحه في تطبيق سابق."},
                            {"what": "تكييف التنفيذ مع البنية التحتية المحلية.",
                             "why": "البنية التحتية المحلية تحدد متطلبات التطبيق العملية."},
                            {"what": "تعديل التنفيذ وفق الميزانية المحلية.",
                             "why": "الموارد المتاحة تؤثر في نطاق التنفيذ ومدته."},
                            {"what": "تكييف التطبيق مع القدرة المؤسسية المحلية.",
                             "why": "نجاح التنفيذ يعتمد على القدرات التقنية والإدارية المحلية."}
                        ]
                    }

                print("Adaptive Gemini API error:", e)
                return {
                    "adaptive_solution_en": reference_solution_name,
                    "adaptive_solution_ar": "الحل المتكيف غير متوفر حاليًا.",
                    "estimated_success": estimated_success,
                    "estimated_duration": estimated_duration,
                    "budget_level_en": country_info.get("Budget_Level", "Unknown"),
                    "budget_level_ar": "غير متوفر حاليًا",
                    "adaptation_points_en": [],
                    "adaptation_points_ar": []
                }

        if response is None:
            return {
                "adaptive_solution_en": reference_solution_name,
                "adaptive_solution_ar": "الحل المتكيف غير متوفر حاليًا.",
                "estimated_success": estimated_success,
                "estimated_duration": estimated_duration,
                "budget_level_en": country_info.get("Budget_Level", "Unknown"),
                "budget_level_ar": "غير متوفر حاليًا",
                "adaptation_points_en": [],
                "adaptation_points_ar": []
            }

        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "")

        if response_text.endswith("```"):
            response_text = response_text.replace("```", "")

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        response_text = response_text.strip()

        try:
            adaptive = json.loads(response_text)
            print("=" * 60)
            print(type(adaptive["adaptation_points_en"]))
            print(adaptive["adaptation_points_en"])
            print(type(adaptive["adaptation_points_en"][0]))
            print(adaptive["adaptation_points_en"][0])
            print("=" * 60)
            adaptive_result = {
                "adaptive_solution_en": adaptive.get(
                    "adaptive_solution_en",
                    reference_solution_name
                ),

                "adaptive_solution_ar": adaptive.get(
                    "adaptive_solution_ar",
                    "الحل المتكيف غير متوفر حاليًا."
                ),

                "estimated_success": estimated_success,

                "estimated_duration": estimated_duration,

                "budget_level_en": adaptive.get(
                    "budget_level_en",
                    country_info.get("Budget_Level", "Unknown")
                ),

                "budget_level_ar": adaptive.get(
                    "budget_level_ar",
                    "غير متوفر"
                ),

                "adaptation_points_en": adaptive.get(
                    "adaptation_points_en",
                    []
                ),

                "adaptation_points_ar": adaptive.get(
                    "adaptation_points_ar",
                    []
                )
            }
            return adaptive_result

        except Exception as e:

            print("=" * 60)
            print("ADAPTIVE ENGINE ERROR")
            print(e)
            print(response_text)
            print("=" * 60)

            return {

                "adaptive_solution": reference_solution_name,

                "estimated_success": reference_success,

                "estimated_duration": reference_duration,

                "budget_level": country_info.get(
                    "Budget_Level",
                    "Unknown"
                ),

                "adaptation_points": [

                    "Adaptive AI unavailable."

                ]

            }

    

    def calculate_success_rate(
        self,
        reference_success,
        compatibility
    ):

        success = reference_success * (compatibility / 100)

        success = round(success)

        success = max(success, 35)

        success = min(success, 99)

        return success

    def calculate_duration(
        self,
        reference_duration,
        country
    ):

        duration = reference_duration

        if country.get("Economy_Level") in ["Low", "Very Low"]:
            duration += 2

        if country.get("Technology_Level") in ["Low", "Very Low"]:
            duration += 2

        if country.get("Infrastructure_Level") in ["Low", "Very Low"]:
            duration += 1

        if country.get("Education_Level") == "Low":
            duration += 1

        return duration