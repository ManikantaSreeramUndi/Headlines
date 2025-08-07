import requests
from bs4 import BeautifulSoup

def scrape_news_headlines(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    potential_headline_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'a', 'p'])
    for tag in potential_headline_tags:
        if tag.name in ['h1', 'h2', 'h3', 'h4'] and tag.get_text(strip=True):
            headlines.append(tag.get_text(strip=True))
        elif tag.name == 'a' and 'news' in tag.get('href', '').lower() and tag.get_text(strip=True) and len(tag.get_text(strip=True)) > 10:
            headlines.append(tag.get_text(strip=True))
        elif tag.name == 'p' and 'headline' in tag.get('class', []):
             headlines.append(tag.get_text(strip=True))

    return list(set(headlines))

def save_headlines_to_file(headlines, filename="headlines.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for headline in headlines:
                f.write(headline + '\n')
        print(f"Headlines saved to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    news_url = "https://www.bbc.com/news"
    print(f"Scraping headlines from: {news_url}")
    scraped_headlines = scrape_news_headlines(news_url)

    if scraped_headlines:
        for i, headline in enumerate(scraped_headlines[:10]):
            print(f"{i+1}. {headline}")
        save_headlines_to_file(scraped_headlines)
    else:
        print("No headlines found or an error occurred.")