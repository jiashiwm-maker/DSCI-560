from bs4 import BeautifulSoup
import csv
from pathlib import Path

def news_extract(soup):
    results = []
    for li in soup.select("ul.LatestNews-list > li.LatestNews-item"):
        time = li.select_one("time.LatestNews-timestamp")
        a = li.select_one("a.LatestNews-headline")
        results.append({
            "LatestNews-timestamp": time.get_text(strip=True) if time else "",
            "title": a.get_text(strip=True),
            "link": a.get("href", "").strip(),
        })
        
    print(f"Extracted {len(results)} news items.")
    return results

def market_extract(soup):
    results = []
    for a in soup.select("a.MarketCard-container"):
        symbol = a.find("span", class_="MarketCard-symbol")
        stock_position = a.find("span", class_="MarketCard-stockPosition")
        changes_percentage = a.find("span", class_="MarketCard-changesPct")
        results.append({
            "MarketCard-symbol": symbol.get_text(strip=True),
            "MarketCard-stockPosition": stock_position.get_text(strip=True),
            "MarketCard-changesPct": changes_percentage.get_text(strip=True)
        })
    
    print(f"Extracted {len(results)} market items.")
    return results  

def main():
    raw_data_dir = "../data/raw_data/web_data.html"
    processed_data_folder = "../data/processed_data/"
    market_dir = processed_data_folder + "market_data.csv"
    news_dir = processed_data_folder + "news_data.csv"
    
    html = Path(raw_data_dir).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    news_data = news_extract(soup)
    with open(news_dir, "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["LatestNews-timestamp", "title", "link"])
        w.writeheader()
        w.writerows(news_data)
    print(f"News data saved to {news_dir}")

    market_data = market_extract(soup)
    with open(market_dir, "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["MarketCard-symbol", "MarketCard-stockPosition", "MarketCard-changesPct"])
        w.writeheader()
        w.writerows(market_data)
    print(f"Market data saved to {market_dir}")

if __name__ == "__main__":
    main()