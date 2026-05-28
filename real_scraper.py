import csv
import requests
from bs4 import BeautifulSoup

def scrape_real_books():
    url = "https://books.toscrape.com"
    print(f"Fetching live data from {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch book data: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print("No books found. The page structure may have changed.")
        return

    scraped_books = []
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        price = float(price_text.replace("£", "").strip())
        scraped_books.append([title, price])

    with open("real_books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "price"])
        writer.writerows(scraped_books)

    print(f"Success! {len(scraped_books)} books saved to real_books.csv")

if __name__ == "__main__":
    scrape_real_books()