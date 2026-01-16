import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        

def main():
    target_url = "https://www.cnbc.com/world/?region=world"
    raw_data_dir = "../data/raw_data/web_data.html"
    
    soup = scrape_website(target_url)
    
    with open(raw_data_dir, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print(f"Web page content saved to {raw_data_dir}")
    

if __name__ == "__main__":
    main()    