import os
import time
import urllib.parse
import csv
import random
import requests
from bs4 import BeautifulSoup

# Base URL of the bookstore website
BASE_URL = "http://books.toscrape.com/"

# A list of common User-Agents to rotate and avoid blocks (Aesthetic & Best Practice)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def get_soup(url, retries=3, delay=2):
    """
    Fetches the HTML content of a URL with random User-Agent rotation
    and a robust retry mechanism for unstable network connections.
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                print(f"    [-] Status code {response.status_code} for {url}. Attempt {attempt}/{retries}")
        except Exception as e:
            print(f"    [-] Connection error on attempt {attempt}/{retries} for {url}: {e}")
        
        # Wait before retrying
        if attempt < retries:
            time.sleep(delay)
            
    print(f"[-] Failed to fetch {url} after {retries} attempts.")
    return None

def scrape_all_books():
    """
    Scrapes all books from books.toscrape.com category by category
    and returns a list of dictionaries containing book details.
    """
    print("=" * 60)
    print("      WEB SCRAPER & CRAWLER - CODEALPHA TASK 1")
    print("=" * 60)
    print("[+] Connecting to books.toscrape.com...")
    
    soup = get_soup(BASE_URL)
    if not soup:
        print("[-] Could not retrieve main page. Exiting.")
        return []

    # 1. Navigating HTML Structure: Extracting Category URLs
    # The categories are located on the left sidebar inside a <div> with class 'side_categories'
    # Structure: div.side_categories -> ul -> li -> ul -> li -> a
    categories_div = soup.find("div", class_="side_categories")
    if not categories_div:
        print("[-] Could not find the side_categories section.")
        return []
    
    category_links = categories_div.find("ul").find("li").find("ul").find_all("a")
    print(f"[+] Found {len(category_links)} book categories to scrape.")
    
    all_books = []
    failed_categories = []
    
    for index, link in enumerate(category_links, 1):
        category_name = link.get_text(strip=True)
        category_relative_url = link["href"]
        # Resolve relative URL to absolute URL
        category_url = urllib.parse.urljoin(BASE_URL, category_relative_url)
        
        print(f"[+] [{index}/{len(category_links)}] Scraping category: {category_name}")
        
        current_page_url = category_url
        category_book_count = 0
        
        while current_page_url:
            cat_soup = get_soup(current_page_url)
            if not cat_soup:
                failed_categories.append(category_name)
                break
                
            # 2. Handling DOM Structure: Extracting individual book elements
            # Each book card is wrapped in an <article> tag with class 'product_pod'
            books = cat_soup.find_all("article", class_="product_pod")
            for book in books:
                # A. Extract Title
                # The full title is stored inside the 'title' attribute of the <a> tag inside <h3>
                title_tag = book.find("h3").find("a")
                title = title_tag["title"] if title_tag.has_attr("title") else title_tag.get_text(strip=True)
                
                # B. Extract Price
                # Price is inside a <p> tag with class 'price_color'
                price_tag = book.find("p", class_="price_color")
                price_text = price_tag.get_text(strip=True) if price_tag else "£0"
                clean_price = price_text.replace("£", "").replace("Â", "").strip()
                try:
                    price = float(clean_price)
                except ValueError:
                    price = 0.0
                
                # C. Extract and Map Rating
                # Rating is represented as a text class inside a <p> tag (e.g. class="star-rating Three")
                rating_tag = book.find("p", class_="star-rating")
                rating_classes = rating_tag["class"] if rating_tag else []
                rating_word = [c for c in rating_classes if c != "star-rating"]
                rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                rating = rating_map.get(rating_word[0], 0) if rating_word else 0
                
                # D. Extract Availability
                # Availability is inside a <p> tag with class 'instock availability'
                availability_tag = book.find("p", class_="instock availability")
                availability = availability_tag.get_text(strip=True) if availability_tag else "Unknown"
                
                all_books.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Availability": availability,
                    "Category": category_name
                })
                category_book_count += 1
                
            # E. Web Navigation (Pagination)
            # Find the 'next' button container <li class="next"> with link pointing to next page
            next_tag = cat_soup.find("li", class_="next")
            if next_tag:
                next_relative_url = next_tag.find("a")["href"]
                current_page_url = urllib.parse.urljoin(current_page_url, next_relative_url)
            else:
                current_page_url = None
                
            # Sleep delay (polite crawling practice)
            time.sleep(0.05)
            
        print(f"    [i] Scraped {category_book_count} books in {category_name}.")
            
    print(f"\n[+] Scraping complete! Scraped {len(all_books)} books in total.")
    if failed_categories:
        print(f"[!] Warning: Failed to connect to categories: {', '.join(failed_categories)}")
        
    return all_books, failed_categories

def save_to_csv(books_data, filepath):
    """
    Saves the list of books to a CSV file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fields = ["Title", "Price", "Rating", "Availability", "Category"]
    
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(books_data)
        print(f"[+] Successfully saved dataset to {filepath}")
    except Exception as e:
        print(f"[-] Error saving to CSV: {e}")

def generate_report(total_books, elapsed_time, failed_cats):
    """
    Generates a local report documenting the web scraping run statistics.
    """
    report_path = os.path.join(os.path.dirname(__file__), "scraping_report.txt")
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("      CODEALPHA WEB SCRAPING DATA QUALITY REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Scrape Status: {'Successful' if not failed_cats else 'Partial Completion'}\n")
            f.write(f"Total Books Scraped: {total_books}\n")
            f.write(f"Execution Duration: {elapsed_time:.2f} seconds\n")
            f.write(f"Average Speed: {total_books / (elapsed_time if elapsed_time > 0 else 1):.2f} books/second\n")
            if failed_cats:
                f.write(f"Failed Categories Count: {len(failed_cats)}\n")
                f.write(f"Failed Categories List: {', '.join(failed_cats)}\n")
            else:
                f.write("Failed Categories: None (All 50 categories crawled successfully)\n")
            f.write("=" * 50 + "\n")
        print(f"[+] Scraper run report generated at: {report_path}")
    except Exception as e:
        print(f"[-] Failed to generate report: {e}")

if __name__ == "__main__":
    start_time = time.time()
    books, failed_cats = scrape_all_books()
    if books:
        output_path = os.path.join(os.path.dirname(__file__), "raw_books_data.csv")
        save_to_csv(books, output_path)
    
    elapsed_time = time.time() - start_time
    generate_report(len(books), elapsed_time, failed_cats)
    print(f"[i] Total execution time: {elapsed_time:.2f} seconds")
