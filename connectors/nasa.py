import requests
from config import NASA_API_KEY


def get_nasa_events():

    url = (
        "https://eonet.gsfc.nasa.gov/api/v3/events"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    return data.get("events", [])

CATEGORY_MAP = {

    "Wildfires": "Wildfires",

    "Floods": "Floods",

    "Volcanoes": "Volcano",

    "Drought": "Drought",

    "Severe Storms": "Cyclone",

    "Sea and Lake Ice": "Climate Change",

    "Landslides": "Landslide"

}

def get_nasa_problems(country=None):

    events = get_nasa_events()

    problems = []

    for event in events:

        title = event["title"]

        # إذا تم اختيار دولة، نتجاهل الأحداث التي لا تخصها
        if country:

            if country.lower() not in title.lower():
                continue

        category = event["categories"][0]["title"]

        if category in CATEGORY_MAP:

            problems.append({

                "problem": CATEGORY_MAP[category],

                "title": title,

                "source": "NASA"

            })

    return problems