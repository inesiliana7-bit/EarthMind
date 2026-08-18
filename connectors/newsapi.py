import requests

API_KEY = "0709c54084a746fe957aff4146b7b81a"

def get_news(country):

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={country}"
        f"&language=en"
        f"&sortBy=publishedAt"
        f"&pageSize=20"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    if data["status"] != "ok":
        return []

    return data["articles"]