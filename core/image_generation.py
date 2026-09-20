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

    visual_anchors = city_data.get(
        "visual_anchors",
        []
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

    visual_anchors_text = "\n".join(
        f"- {anchor}"
        for anchor in visual_anchors
    )


    # =========================================================
    # EARTHMIND VISUAL SIMULATION PROMPT
    # =========================================================

    prompt = f"""
Create a highly realistic strategic future visualization of {city}
in {country} after successful implementation of the following
adaptive solution.

CITY: {city}
COUNTRY: {country}
PROBLEM: {problem}
SOLUTION: {solution}
SECTOR: {sector}
PROJECTED EFFECTS: {", ".join(projected_effects)}

CITY IDENTITY:
Region: {region}
Geography: {geographic_context}
Climate: {climate_context}
Terrain: {terrain_context}
Water: {water_context}
Urban form: {urban_context}
Architecture: {architectural_identity}
Infrastructure: {infrastructure_context}
Visual identity: {visual_identity}

CITY IDENTITY ANCHORS:
{visual_anchors_text}

VISUAL PRIORITIES:
{visual_priorities_text}

FORBIDDEN FEATURES:
{forbidden_text}

Show a plausible near-future transformation of the REAL existing city.

Preserve the city's authentic geography, climate, terrain, urban
density, architecture, infrastructure and local visual identity.

Use the city identity anchors as recognition anchors.
The image must look specifically like {city}, not like a generic
city from the same region.

The solution must be clearly visible through its physical effects
on the city and must improve the selected sector.

The scene must look like a professional government urban-planning
simulation or high-end architectural visualization.

Photorealistic, cinematic natural lighting, realistic materials,
credible infrastructure, physically plausible development,
high-end strategic visualization.

Do NOT create a generic futuristic city.
Do NOT change the geography.
Do NOT replace local architecture with foreign architecture.
Do NOT mix features from another city.
Do NOT invent landmarks.
Do NOT use science-fiction architecture, flying buildings,
fantasy landmarks, megastructures, random skyscrapers,
fictional monuments, text, captions, logos, watermarks or labels.

The final image must clearly represent {city}, {country},
and visually communicate the consequences of implementing
the proposed solution.
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