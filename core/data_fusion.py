from connectors.gnews import get_news
from connectors.nasa import get_nasa_problems


def collect_all_sources(country):

    data = {}

    # GNews
    try:
        data["news"] = get_news(country)
    except:
        data["news"] = []

    # NASA
    try:
        data["nasa"] = get_nasa_problems(country)
    except:
        data["nasa"] = []

    print(data)

    return data