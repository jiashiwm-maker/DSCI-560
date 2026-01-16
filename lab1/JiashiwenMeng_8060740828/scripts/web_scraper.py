import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
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