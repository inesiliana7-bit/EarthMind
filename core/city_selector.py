import os
import json
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


CITY_MODEL = "gemini-2.5-flash"


class CitySelector:

    def select_city(
        self,
        country,
        country_info,
        problem,
        adaptive_solution,
        sector
    ):

        prompt = f"""
You are EarthMind Global Representative City Intelligence Engine.

EarthMind is a strategic decision-support platform that analyzes
national problems and simulates how adaptive solutions could affect
real-world locations.

Your task is to select ONE REAL EXISTING CITY anywhere in the world.

The selected city must belong to the specified country.

You are NOT generating an image.

You are producing a reliable city intelligence profile that will
later be passed to a separate image-generation system.

==================================================
COUNTRY
==================================================

{country}


==================================================
COUNTRY PROFILE
==================================================

{json.dumps(
    country_info,
    ensure_ascii=False,
    default=str
)}


==================================================
DETECTED PROBLEM
==================================================

{problem}


==================================================
ADAPTIVE SOLUTION
==================================================

{adaptive_solution}


==================================================
STRATEGIC SECTOR
==================================================

{sector}


==================================================
CITY SELECTION OBJECTIVE
==================================================

Select the city that provides the strongest real-world visual and
strategic representation of the specific problem and solution.

Do NOT automatically select the capital.

Do NOT automatically select the largest city.

Do NOT select a city simply because it is famous.

The city must be selected because its real geographic, urban,
environmental, infrastructural or socioeconomic characteristics
make it highly relevant to the simulation.

Consider:

1. Relevance to the detected problem
2. Relevance to the adaptive solution
3. Geographic relevance
4. Environmental relevance
5. Infrastructure relevance
6. Population and urban importance
7. National strategic importance
8. Ability to visually demonstrate the consequences of the solution
9. Availability of reliable geographic knowledge
10. Representativeness of the selected city for this particular
    EarthMind scenario


==================================================
GLOBAL ACCURACY RULES
==================================================

The system must work for ANY country in the world.

The selected city MUST:

- be a real existing city
- be located inside the specified country
- have a recognized geographic identity
- have plausible and established urban characteristics

NEVER invent:

- cities
- rivers
- lakes
- mountains
- coastlines
- deserts
- forests
- landmarks
- infrastructure
- architectural features

Do not confuse national characteristics with city characteristics.

For example:

A country may contain desert regions, but that does NOT mean every
city in that country is located in a desert.

A country may have mountains, but the selected city may be on a plain.

Use city-level geographic reality whenever possible.


==================================================
VISUAL SIMULATION RULE
==================================================

The final image will represent:

CURRENT REAL CITY
        +
ADAPTIVE SOLUTION
        ↓
PLAUSIBLE NEAR-FUTURE CITY

The city must remain recognizable as the same real place.

The solution may transform:

- infrastructure
- water systems
- energy systems
- transportation
- public spaces
- buildings
- environmental conditions
- resource management
- resilience systems

But the transformation must remain physically plausible.

Do NOT turn the city into science fiction.


==================================================
FORBIDDEN INVENTIONS
==================================================

Identify important geographic or architectural features that the
image generator must NOT invent.

Examples:

- major river through the city when none exists
- ocean when the city is inland
- desert dunes when the city is not adjacent to a desert
- tropical vegetation in a cold climate
- mountains immediately surrounding a flat city
- famous landmarks that are not actually present
- unrealistic skyscraper clusters
- fictional infrastructure


==================================================
OUTPUT
==================================================

Return ONLY a valid JSON object.

Use exactly these keys:

{{
    "city": "",
    "country": "",
    "selection_reason": "",
    "region": "",
    "geographic_context": "",
    "climate_context": "",
    "terrain_context": "",
    "water_context": "",
    "urban_context": "",
    "architectural_identity": "",
    "infrastructure_context": "",
    "visual_identity": "",
    "forbidden_geographic_features": [],
    "visual_priorities": [],
    "confidence": 0
}}


==================================================
FIELD DEFINITIONS
==================================================

city:

The selected real city.


country:

The country containing the selected city.


selection_reason:

Explain why this specific city is more strategically relevant
than alternative cities for the given problem and solution.


region:

The real geographic region where the city is located.


geographic_context:

Concise factual description of the city's actual geography.


climate_context:

Realistic local climate characteristics.


terrain_context:

Actual terrain characteristics of the city.


water_context:

Describe actual water-related geographic characteristics.

Only mention:

- sea
- ocean
- river
- lake
- reservoir
- coastline
- water infrastructure

when they are genuinely relevant and geographically plausible.


urban_context:

Describe the city's real urban structure and density.


architectural_identity:

Describe recognizable architectural characteristics.

Do not invent famous landmarks.


infrastructure_context:

Describe real infrastructure characteristics relevant to the
simulation.


visual_identity:

Describe the visual characteristics that should make the generated
image recognizable as this city.


forbidden_geographic_features:

List geographic or architectural elements that should explicitly
NOT appear in the generated image.


visual_priorities:

List between 3 and 6 visual elements that should communicate
the adaptive solution.


confidence:

Integer between 0 and 100.

This represents confidence in the city selection and geographic
context.

==================================================

Return JSON ONLY.
"""


        response = None


        for attempt in range(3):

            try:

                print(
                    f"City Selector attempt {attempt + 1}/3"
                )

                response = client.models.generate_content(
                    model=CITY_MODEL,
                    contents=prompt
                )

                break

            except Exception as e:

                print(
                    f"City Selector attempt {attempt + 1} failed:",
                    e
                )

                if attempt == 2:
                    raise

                time.sleep(3)


        if response is None:

            raise RuntimeError(
                "City Selector did not receive a Gemini response."
            )


        text = response.text.strip()


        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()


        if not text.startswith("{"):

            raise RuntimeError(
                "City Selector returned invalid JSON."
            )


        try:

            result = json.loads(text)

        except json.JSONDecodeError as e:

            print("INVALID CITY SELECTOR JSON:")
            print(text)

            raise RuntimeError(
                f"City Selector JSON parsing failed: {e}"
            )


        required_keys = [

            "city",
            "country",
            "selection_reason",
            "region",
            "geographic_context",
            "climate_context",
            "terrain_context",
            "water_context",
            "urban_context",
            "architectural_identity",
            "infrastructure_context",
            "visual_identity",
            "forbidden_geographic_features",
            "visual_priorities",
            "confidence"

        ]


        for key in required_keys:

            if key not in result:

                raise RuntimeError(
                    f"City Selector missing field: {key}"
                )


        if not result["city"]:

            raise RuntimeError(
                "City Selector returned an empty city."
            )


        if not result["country"]:

            result["country"] = country


        try:

            result["confidence"] = int(
                result["confidence"]
            )

        except (
            TypeError,
            ValueError
        ):

            result["confidence"] = 0


        result["confidence"] = max(
            0,
            min(
                100,
                result["confidence"]
            )
        )


        return result