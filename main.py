import feedparser
import yaml
import requests
from datetime import datetime

with open("sources.yaml", "r") as file:
    config = yaml.safe_load(file)

sources = config["sources"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

keywords = ["review", "driven", "tested", "first drive", "road test"]

reviews = []

for source in sources:
    print(f"\nTikrinamas šaltinis: {source['name']}")

    response = requests.get(source["url"], headers=headers, timeout=20)
    feed = feedparser.parse(response.text)

    print("Rasta įrašų:", len(feed.entries))

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = getattr(entry, "summary", "")

        title_lower = title.lower()

        if any(keyword in title_lower for keyword in keywords):
            reviews.append({
                "source": source["name"],
                "title": title,
                "link": link,
                "summary": summary
            })

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Automobilių apžvalgų suvestinė</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            line-height: 1.6;
            background: #f5f5f5;
            color: #222;
        }}
        h1 {{
            color: #111;
        }}
        .meta {{
            color: #666;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 22px;
            margin-bottom: 18px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .source {{
            font-size: 13px;
            color: #777;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        a {{
            color: #0057b8;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Automobilių apžvalgų suvestinė</h1>
    <div class="meta">
        Sugeneruota: {datetime.now().strftime("%Y-%m-%d %H:%M")}<br>
        Rasta apžvalgų: {len(reviews)}
    </div>
"""

for review in reviews:
    html += f"""
    <div class="card">
        <div class="source">{review['source']}</div>
        <h2>{review['title']}</h2>
        <p>{review['summary']}</p>
        <p><a href="{review['link']}" target="_blank">Skaityti straipsnį →</a></p>
    </div>
    """

html += """
</body>
</html>
"""

with open("report.html", "w", encoding="utf-8") as file:
    file.write(html)

print(f"\nBaigta. Sukurtas failas: report.html")
print(f"Rasta apžvalgų: {len(reviews)}")
