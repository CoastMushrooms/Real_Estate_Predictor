import csv
import requests
from bs4 import BeautifulSoup

def scrape_properties():
    try:
        with open('mock_listings.html', 'r') as file:
            html_content = file.read()
    except FileNotFoundError:
        print("Error: 'mock_listings.html' not found. Please create it to scrape properties.")
        return
        
    soup = BeautifulSoup(html_content, "html.parser")
    property_cards = soup.find_all("div", class_="property-card")
    
    scraped_data = []
    for card in property_cards:
        price_text = card.find("span", class_="price").text
        price = int(price_text.replace("$", "").replace(",", ""))
        
        sqft_text = card.find("span", class_="sqft").text
        sqft = int(sqft_text.replace(" sqft", ""))
        
        beds_text = card.find("span", class_="beds").text
        beds = int(beds_text.replace(" bedrooms", ""))
        
        scraped_data.append([sqft, beds, price])
        
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sqft", "beds", "price"])
        writer.writerows(scraped_data)
        
    print("Success! Property data saved to data.csv")


def scrape_real_books():
    url = "https://books.toscrape.com"
    print(f"Fetching live data from {url}...")
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch book data: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    scraped_books = []
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        price = float(price_text.replace("£", ""))
        scraped_books.append([title, price])
        
    with open("real_books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "price"])
        writer.writerows(scraped_books)
        
    print("Success! Live book data saved to real_books.csv")


if __name__ == "__main__":
    scrape_properties()
    scrape_real_books()