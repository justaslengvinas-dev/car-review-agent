import feedparser
import yaml

# Užkrauname šaltinius iš YAML failo
with open("sources.yaml", "r") as file:
    config = yaml.safe_load(file)

sources = config["sources"]

# Einame per visus RSS šaltinius
for source in sources:
    print(f"\nTikrinamas šaltinis: {source['name']}")

    feed = feedparser.parse(source["url"])

    # Paimame pirmus 5 straipsnius
    for entry in feed.entries[:5]:
        print("-" * 50)
        print("Pavadinimas:", entry.title)
        print("Nuoroda:", entry.link)
