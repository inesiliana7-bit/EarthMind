import os
import base64
import requests

from dotenv import load_dotenv


load_dotenv()


CLOUDFLARE_ACCOUNT_ID = os.getenv(
    "CLOUDFLARE_ACCOUNT_ID"
)

CLOUDFLARE_API_TOKEN = os.getenv(
    "CLOUDFLARE_API_TOKEN"
)


if not CLOUDFLARE_ACCOUNT_ID:
    raise RuntimeError(
        "CLOUDFLARE_ACCOUNT_ID is missing from .env"
    )


if not CLOUDFLARE_API_TOKEN:
    raise RuntimeError(
        "CLOUDFLARE_API_TOKEN is missing from .env"
    )


IMAGE_MODEL = "@cf/black-forest-labs/flux-1-schnell"


def generate_future_city_image(
    country,
    city_data,
    problem,
    solution,
    sector,
    projected_effects
):

    # =========================================================
    # CITY INTELLIGENCE
    # =========================================================

    city = city_data.get(
        "city",
        "Unknown city"
    )

    region = city_data.get(
        "region",
        ""
    )

    geographic_context = city_data.get(
        "geographic_context",
        ""
    )

    climate_context = city_data.get(
        "climate_context",
        ""
    )

    terrain_context = city_data.get(
        "terrain_context",
        ""
    )

    water_context = city_data.get(
        "water_context",
        ""
    )

    urban_context = city_data.get(
        "urban_context",
        ""
    )

    architectural_identity = city_data.get(
        "architectural_identity",
        ""
    )

    infrastructure_context = city_data.get(
        "infrastructure_context",
        ""
    )

    visual_identity = city_data.get(
        "visual_identity",
        ""
    )

    forbidden_features = city_data.get(
        "forbidden_geographic_features",
        []
    )

    visual_priorities = city_data.get(
        "visual_priorities",
        []
    )


    # =========================================================
    # FORMAT LISTS
    # =========================================================

    effects_text = "\n".join(
        f"- {effect}"
        for effect in projected_effects
    )


    forbidden_text = "\n".join(
        f"- {feature}"
        for feature in forbidden_features
    )


    visual_priorities_text = "\n".join(
        f"- {priority}"
        for priority in visual_priorities
    )


    # =========================================================
    # EARTHMIND VISUAL SIMULATION PROMPT
    # =========================================================

    prompt = f"""
You are the visual simulation engine of EarthMind.

Your task is to generate a highly realistic professional
strategic visualization of a REAL existing city.

The image must show the selected city after the successful
implementation of an adaptive solution proposed by EarthMind.

This is NOT a generic futuristic city.

This is NOT science fiction.

This is a plausible near-future transformation of a real city.


============================================================
IDENTITY
============================================================

COUNTRY:
{country}

CITY:
{city}

REGION:
{region}


============================================================
CURRENT CITY GEOGRAPHY
============================================================

Geographic context:
{geographic_context}

Climate:
{climate_context}

Terrain:
{terrain_context}

Water context:
{water_context}


============================================================
CURRENT URBAN CHARACTER
============================================================

Urban context:
{urban_context}

Architectural identity:
{architectural_identity}

Infrastructure:
{infrastructure_context}

Visual identity:
{visual_identity}


============================================================
EARTHMIND SCENARIO
============================================================

PROBLEM:
{problem}

ADAPTIVE SOLUTION:
{solution}

STRATEGIC SECTOR:
{sector}


PROJECTED EFFECTS:
{effects_text}


============================================================
VISUAL PRIORITIES
============================================================

The following elements should be visually emphasized:

{visual_priorities_text}


============================================================
GEOGRAPHIC ACCURACY
============================================================

The city must remain geographically plausible.

Preserve:

- the real terrain
- the real climate
- the real urban density
- the real geographic setting
- the real architectural character
- the real relationship between the city and surrounding landscape

Do not transform the city into another geographic environment.

Do not replace the city's real geography with generic futuristic
city imagery.


============================================================
FORBIDDEN FEATURES
============================================================

The following elements MUST NOT appear unless they genuinely
exist in the selected city:

{forbidden_text}


============================================================
TRANSFORMATION LOGIC
============================================================

The image should communicate:

REAL CITY
+
REAL LOCAL CONDITIONS
+
EARTHMIND ADAPTIVE SOLUTION
=
PLAUSIBLE NEAR-FUTURE RESULT


The transformation must be visible through realistic changes
to infrastructure, public spaces, environmental conditions,
resource management, buildings, transportation, water systems,
energy systems, or other elements directly related to the
proposed solution.


============================================================
IMPORTANT VISUAL RULE
============================================================

The solution must be visually obvious.

Do not simply create a beautiful city.

Show HOW the solution changed the city.

For example, if the solution concerns water management:

- intelligent water infrastructure
- efficient water distribution
- repaired infrastructure
- reduced visible water waste
- realistic monitoring systems
- water-efficient public spaces
- resilient water infrastructure

should appear where geographically and architecturally plausible.


============================================================
REALISM
============================================================

Style:

- photorealistic
- high-end architectural visualization
- professional urban planning visualization
- realistic infrastructure
- cinematic natural lighting
- physically plausible materials
- realistic proportions
- realistic streets
- realistic buildings
- realistic vegetation
- realistic atmosphere
- sophisticated strategic simulation aesthetic
- believable near-future development


============================================================
DO NOT GENERATE
============================================================

- science-fiction cities
- flying buildings
- impossible architecture
- fictional landmarks
- unrealistic megastructures
- excessive skyscrapers
- fantasy landscapes
- exaggerated futuristic technology
- artificial-looking environments
- random futuristic city skylines
- text
- captions
- labels
- logos
- watermarks


============================================================
CITY RECOGNITION
============================================================

A person familiar with {city}, {country} should be able to
recognize the geographic and architectural character of the city.

The generated image should feel like:

"{city} in a plausible successful future"

and NOT:

"a random futuristic city."


============================================================
FINAL REQUIREMENT
============================================================

Generate ONE coherent photorealistic scene.

Prioritize geographic accuracy, urban identity and the visible
consequences of the EarthMind solution over futuristic aesthetics.

The final result must look like a professional strategic
future-city simulation prepared for government decision-making.
"""


    # =========================================================
    # CLOUDFLARE REQUEST
    # =========================================================

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
        f"{IMAGE_MODEL}"
    )


    response = requests.post(
        url,
        headers={
            "Authorization":
                f"Bearer {CLOUDFLARE_API_TOKEN}",

            "Content-Type":
                "application/json",
        },
        json={
            "prompt": prompt,
            "steps": 4,
        },
        timeout=120,
    )


    # =========================================================
    # HTTP ERROR
    # =========================================================

    if response.status_code != 200:

        raise RuntimeError(
            "Cloudflare image generation failed "
            f"({response.status_code}): "
            f"{response.text}"
        )


    # =========================================================
    # API RESPONSE
    # =========================================================

    result = response.json()


    if not result.get("success"):

        raise RuntimeError(
            "Cloudflare image generation failed: "
            f"{result}"
        )


    image_data = (
        result
        .get("result", {})
        .get("image")
    )


    if not image_data:

        raise RuntimeError(
            "Cloudflare did not return an image."
        )


    # =========================================================
    # RETURN IMAGE BYTES
    # =========================================================

    return base64.b64decode(
        image_data
    )