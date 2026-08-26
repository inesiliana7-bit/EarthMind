import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=GEMINI_API_KEY)

IMAGE_MODEL = "gemini-3.1-flash-lite-image"


def generate_future_city_image(
    country,
    city,
    problem,
    solution,
    sector,
    projected_effects
):
    effects_text = "\n".join(
        f"- {effect}" for effect in projected_effects
    )

    prompt = f"""
You are the visual simulation engine of EarthMind.

Create a highly realistic 3D visualization showing how
{city}, {country} could look after successfully implementing
an adaptive solution proposed by EarthMind.

COUNTRY:
{country}

CITY:
{city}

PROBLEM:
{problem}

ADAPTIVE SOLUTION:
{solution}

STRATEGIC SECTOR:
{sector}

PROJECTED EFFECTS:
{effects_text}

IMPORTANT:
The image must represent the consequences of the solution,
not simply a generic futuristic city.

Preserve recognizable characteristics of the city,
its geographic context, urban identity and realistic
architectural character.

Visually express the positive effects of the proposed solution
through the city's infrastructure, environment, public spaces,
transportation, water systems, energy systems, buildings,
or other elements relevant to the solution.

Style:
- photorealistic high-end 3D visualization
- realistic urban planning
- cinematic but scientifically credible
- detailed architecture
- realistic infrastructure
- natural lighting
- sophisticated strategic simulation aesthetic
- believable near-future development
- no science-fiction fantasy
- no floating buildings
- no impossible architecture
- no text inside the image
- no logos
- no exaggerated futuristic technology

The result should look like a professional strategic
future-city simulation created for a government decision-support
platform.
"""

    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"]
        )
    )

    for part in response.parts:
        if part.thought:
            continue

        if part.inline_data is not None:
            return part.as_image()

    raise RuntimeError("Gemini did not return an image.")