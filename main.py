import feedparser
import yaml

with open("sources.yaml", "r") as file:
    config = yaml.safe_load(file)

sources = config["sources"]

for source in sources:
    print(f"\nTikrinamas šaltinis: {source['name']}")
    print(f"URL: {source['url']}")

    feed = feedparser.parse(source["url"])

    print("Rasta įrašų:", len(feed.entries))

    if len(feed.entries) == 0:
        print("Šis RSS šaltinis šiuo metu negrąžina įrašų.")
        continue

    for entry in feed.entries[:5]:
        print("-" * 50)
        print("Pavadinimas:", entry.title)
        print("Nuoroda:", entry.link)
