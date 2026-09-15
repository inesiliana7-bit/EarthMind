import os
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NASA_API_KEY = os.getenv("NASA_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
WHO_API_KEY = os.getenv("WHO_API_KEY", "")
FAO_API_KEY = os.getenv("FAO_API_KEY", "")