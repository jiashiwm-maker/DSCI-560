# Get three kinds of online dataset: CSV or Excel, HTML, PDF
# This is an example code for the future final project.
# This code using MTG scenario as a example.

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pdfplumber
import json
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_web_table(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()
    
    table = soup.find("table")
    
    headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
    
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        row = [td.get_text(strip=True) for td in tr.find_all("td")]
        rows.append(row)
    
    return pd.DataFrame(rows, columns=headers)


_SESSION = requests.Session()
_SESSION.headers.update({"User-Agent": "DSCI560-Lab/1.0"})


def get_card_data(url):
    data = _SESSION.get(url).json()
    search_uri = data["search_uri"]
    
    all_cards = []
    while search_uri:
        content = _SESSION.get(search_uri).json()
        all_cards.extend(content["data"])
        search_uri = content.get("next_page") if content.get("has_more") else None
    
    df = pd.DataFrame(all_cards)
    cols = ["name", "mana_cost", "type_line", "oracle_text", "rarity", "set", "collector_number"]
    return df[cols]

def get_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n\n".join(filter(None, pages))

def main():
    url = "https://api.scryfall.com/sets/eoe"
    lands_url = "https://www.17lands.com/card_data?expansion=EOE&format=PremierDraft&start=2025-07-29&view=table"
    data_path = "../data/"
    
    card_path = data_path + "eoe_cards.csv"
    lands_path = data_path + "eoe_lands.csv"
    pdf_path = data_path + "rule.pdf"
    rule_path = data_path + "rule.txt"
    
    card_data = get_card_data(url)
    print("Card Data Sample:")
    print(card_data.head())
    print(f"Total cards: {len(card_data)}")
    
    card_data.to_csv(card_path, index=False)
    
    web_table = get_web_table(lands_url)
    print("17Lands Data Sample:")
    print(web_table.head())
    print(f"Total records: {len(web_table)}")
    
    web_table.to_csv(lands_path, index=False)
    
    pdf_text = get_pdf_text(pdf_path)
    print(f"PDF pages extracted, {len(pdf_text)} characters")
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(pdf_text)

if __name__ == "__main__":
    main()