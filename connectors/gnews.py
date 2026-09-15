import requests
from config import GNEWS_API_KEY


def get_news(country, max_articles=20):
    url = (
        f"https://gnews.io/api/v4/search"
        f"?q={country}"
        f"&lang=en"
        f"&max={max_articles}"
        f"&apikey={GNEWS_API_KEY}"
    )

    try:
        print(url)

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "EarthMind/1.0"
            }
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("GNews Error:", response.status_code)
            return []

        data = response.json()

        articles = []

        for article in data.get("articles", []):
            articles.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"],
                "source": article["source"]["name"]
            })

        print("Number of articles:", len(articles))
        return articles

    except requests.exceptions.RequestException as e:
        print("GNews Network Error:", e)
        return []


if __name__ == "__main__":
    news = get_news("Algeria")
    print(news)