import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_static_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=20)
    return BeautifulSoup(response.text, 'html.parser')

def get_dynamic_content(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "MarketCard-row"))
        )
        return BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()

def main():
    target_url = "https://www.cnbc.com/world/?region=world"
    raw_data_dir = "../data/raw_data/web_data.html"
    
    static_soup = get_static_content(target_url)
    dynamic_soup = get_dynamic_content(target_url)
    
    # Get news
    latest_news = static_soup.find("ul", class_="LatestNews-list")
    # Get market
    market_banner = dynamic_soup.find("div", class_="MarketsBanner-marketData")
    
    with open(raw_data_dir, 'w', encoding='utf-8') as file:
        if market_banner:
            file.write(market_banner.prettify())
            file.write("\n\n")
        if latest_news:
            file.write(latest_news.prettify())
    print(f"Web page content saved to {raw_data_dir}")

if __name__ == "__main__":
    main()