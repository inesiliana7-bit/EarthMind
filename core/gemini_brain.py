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

IMPORTANT CURRENT-CRISIS RULE:

EarthMind must NEVER invent a problem.

The objective is to detect a REAL CURRENT national crisis affecting the selected country,
based ONLY on the provided recent evidence.

If the provided news and NASA/scientific observations do NOT contain sufficient evidence
of a current national problem:

- primary_problem MUST be "No Problem"
- primary_problem_ar MUST be "لا توجد مشكلة حالية"
- secondary_problems MUST be []
- problem_ranking MUST be []
- confidence MUST be 0
- root_cause MUST be "N/A"
- root_cause_ar MUST be "غير متوفر"
- risk_level MUST be "Unknown"
- news_coverage MUST be 0
- scientific_support MUST be 0
- impact_dimensions MUST be []
- future_consequences MUST be ""
- future_consequences_ar MUST be ""
- recommendation MUST be ""
- recommendation_ar MUST be ""
- key_findings MUST be []
- key_findings_ar MUST be []
- data_quality MUST be "Insufficient"

CRITICAL:

If primary_problem is "No Problem":

DO NOT propose any solution.
DO NOT select a reference country.
DO NOT estimate a success rate.
DO NOT estimate an implementation duration.
DO NOT use historical problems as current problems.
DO NOT infer a crisis merely because a problem exists in Available Problems.
DO NOT infer a crisis from a possible future risk, general trend, old event, or isolated keyword.

A problem is CURRENT only when the provided evidence clearly indicates
that the problem is actively affecting the selected country now.

When evidence is insufficient, ALWAYS choose "No Problem".

CITY SELECTION AND VISUAL CONTEXT:

If primary_problem is NOT "No Problem":

1. Identify ONE real city or clearly defined urban region
   in the selected country that is especially relevant
   to the detected problem.

2. The city must be selected because of its real geographic,
   climatic, environmental, urban, infrastructural, or
   socioeconomic characteristics related to the problem.

3. Do NOT select a city randomly.

4. Do NOT assume that the capital city is always the correct city.

5. Do NOT invent a fictional city.

6. Do NOT provide a list of cities.
   Select ONE city only.

7. Create a concise CITY PROFILE for visual simulation.

The CITY PROFILE must contain ONLY information that is
visually relevant to generating a realistic image of the city.

Include:

- city
- region
- geographic_context
- climate_context
- terrain_context
- water_context
- urban_context
- architectural_identity
- infrastructure_context
- visual_identity
- visual_anchors
- forbidden_geographic_features
- visual_priorities

VISUAL IDENTITY ANCHORS:

The CITY PROFILE must also contain "visual_anchors".

"visual_anchors" must contain 3 to 5 concise, real-world visual
elements that strongly help distinguish the selected city from
a generic city in the same country or region.

Choose the anchors dynamically according to the selected city.

Possible anchor types include:
- a well-established real landmark or recognizable built feature
- a distinctive urban form or city layout
- a characteristic geographic feature
- a locally distinctive architectural feature
- a characteristic infrastructure feature

IMPORTANT:

- Never invent a landmark.
- Never use an uncertain landmark as a visual anchor.
- Never mix landmarks or architectural features from different cities.
- Do NOT force a famous landmark if the city does not have a
  reliably known one.
- For smaller or less internationally known cities, prefer
  distinctive urban, geographic, architectural, or infrastructural
  characteristics instead of inventing a landmark.
- Each anchor must be genuinely associated with the selected city.
- The anchors must be visually representable in an image.
- Keep each anchor short and concrete.
- Use 3 to 5 anchors maximum.

The purpose of visual_anchors is to make the generated image
recognizably belong to the selected city rather than producing
a generic city with similar climate or architecture.

Keep the complete city profile concise.
Do NOT exceed approximately 120 words in total.

IMPORTANT:

The city profile will be sent directly to an image-generation
model.

Therefore:
- prioritize real-world visual characteristics
- preserve the authentic identity of the selected city
- describe characteristics that can actually appear in an image
- never turn the city into a generic futuristic city
- never replace local architecture with foreign architecture
- never invent landmarks

If primary_problem is "No Problem":

- city MUST be ""
- city_selection_reason MUST be ""
- city_profile MUST be {{}}

Return:

city
city_selection_reason
city_profile


Return ONLY a valid JSON object.

Example:

{{
"primary_problem": "Wildfires",
"primary_problem_ar": "حرائق الغابات",

"city": "Bejaia",
"city_selection_reason": "The city is relevant because of its Mediterranean climate, mountainous terrain and surrounding forested areas.",
"city_profile": {{
    "region": "Northern Algeria",
    "geographic_context": "Mediterranean coastal city surrounded by mountainous terrain.",
    "climate_context": "Mediterranean climate with hot dry summers.",
    "terrain_context": "Mountainous and forested surroundings.",
    "water_context": "Coastal setting with local water infrastructure.",
    "urban_context": "Dense Algerian coastal urban fabric.",
    "architectural_identity": "North African Mediterranean urban architecture.",
    "infrastructure_context": "Urban roads and emergency-access infrastructure.",
    "visual_identity": "Coastal Algerian city between mountains and sea.",
    "visual_anchors": [
        "Bejaia's mountainous coastal setting",
        "Mediterranean urban coastline",
        "dense North African coastal neighborhoods",
        "surrounding forested mountain slopes"
    ],
    "forbidden_geographic_features": [
        "Dubai-style skyline",
        "Gulf architecture",
        "fictional megastructures"
    ],
    "visual_priorities": [
        "forested mountains",
        "Mediterranean coastline",
        "realistic Algerian urban environment",
        "wildfire prevention infrastructure"
    ]
}},

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
city
city_selection_reason
city_profile
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

            result.setdefault("city", "")
            result.setdefault("city_selection_reason", "")
            result.setdefault("city_profile", {})

            # Ensure city profile always has a valid visual anchor list
            city_profile = result["city_profile"]

            if not isinstance(city_profile, dict):
                city_profile = {}
                result["city_profile"] = city_profile

            city_profile.setdefault("region", "")
            city_profile.setdefault("geographic_context", "")
            city_profile.setdefault("climate_context", "")
            city_profile.setdefault("terrain_context", "")
            city_profile.setdefault("water_context", "")
            city_profile.setdefault("urban_context", "")
            city_profile.setdefault("architectural_identity", "")
            city_profile.setdefault("infrastructure_context", "")
            city_profile.setdefault("visual_identity", "")
            city_profile.setdefault("visual_anchors", [])
            city_profile.setdefault("forbidden_geographic_features", [])
            city_profile.setdefault("visual_priorities", [])

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