from bs4 import BeautifulSoup
import csv
from pathlib import Path

def news_extract(soup):
    news = soup.find("div", attrs={"data-test": "latestNews-0"})
    
    results = []
    for li in news.select("ul.LatestNews-list > li.LatestNews-item"):
        time = li.select_one("time.LatestNews-timestamp")
        a = li.select_one("a.LatestNews-headline")
        results.append({
            "LatestNews-timestamp": time.get_text(strip=True) if time else "",
            "title": a.get_text(strip=True),
            "link": a.get("href", "").strip(),
        })
        
    print(f"Extracted {len(results)} news items.")
        
    return results


def main():
    raw_data_dir = "../data/raw_data/web_data.html"
    processed_data_folder = "../data/processed_data/"
    market_dir = processed_data_folder + "market_data.csv"
    news_dir = processed_data_folder + "news_data.csv"
    
    lines = Path(raw_data_dir).read_text(encoding="utf-8").splitlines(True)
    html = "".join(lines)
    soup = BeautifulSoup(html, "html.parser")
    news_data = news_extract(soup)
    
    with open(news_dir, "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["LatestNews-timestamp", "title", "link"])
        w.writeheader()
        w.writerows(news_data)
    print(f"News data saved to {news_dir}")
    

if __name__ == "__main__":
    main()