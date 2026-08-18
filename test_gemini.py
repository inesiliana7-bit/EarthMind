from core.gemini_brain import GeminiBrain

brain = GeminiBrain()

news = [
    {
        "title": "Massive wildfires spread across Canada",
        "description": "Thousands evacuated as forests continue burning."
    }
]

nasa = [
    {
        "problem": "Wildfires",
        "title": "Wildfire in Canada"
    }
]

result = brain.analyze(
    "Canada",
    news,
    nasa
)

print(result)