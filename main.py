import feedparser
import yaml
import requests

with open("sources.yaml", "r") as file:
    config = yaml.safe_load(file)

sources = config["sources"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for source in sources:
    print(f"\nTikrinamas šaltinis: {source['name']}")
    print(f"URL: {source['url']}")

    response = requests.get(source["url"], headers=headers, timeout=20)

    print("HTTP statusas:", response.status_code)
    print("Atsisiųsta simbolių:", len(response.text))

    feed = feedparser.parse(response.text)

    print("Rasta įrašų:", len(feed.entries))

keywords = ["review", "driven", "tested", "first drive"]

for entry in feed.entries:
    title_lower = entry.title.lower()

    if any(keyword in title_lower for keyword in keywords):
        print("-" * 50)
        print("Pavadinimas:", entry.title)
        print("Nuoroda:", entry.link)
