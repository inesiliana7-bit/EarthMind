from openai import OpenAI
import json
import os


class EarthMindBrain:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def analyze_world(self, country, news, nasa):

        prompt = f"""
You are EarthMind AI.

Country:
{country}

News:
{news}

NASA events:
{nasa}

Your task:

Determine ONLY the MAIN problem currently affecting this country.

Choose ONLY ONE problem.

The answer MUST be JSON only.

{{
"problem":"",
"severity":"",
"confidence":0,
"sector":"",
"summary":"",
"reason":""
}}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        return json.loads(
            response.choices[0].message.content
        )