import requests
from bs4 import BeautifulSoup
import json



BASE_URL = "https://quotes.toscrape.com"

def get_quotes():
    quotes_data = []
    authors_links = set()
    url = "/page/1"

    while url:
        response = requests.get(BASE_URL + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for q in soup.find_all('div', class_='quote'):
            quotes_data.append({
                'tags': [tag.get_text() for tag in q.find_all('a', class_='tag')],
                'autor': q.find('small', class_='author').get_text(),
                'quote': q.find('span', class_='text'). get_text()
            })
            link_tag = q.find('a', string='(about)')
            if link_tag:
                authors_links.add(link_tag['href'])

        next_button = soup.find('li', class_='next')
        url = next_button.find('a')['href'] if next_button else None


    return quotes_data, authors_links

def get_authors(links):
    authors_data = []
    for link in links:
        response = requests.get(BASE_URL + link)
        soup = BeautifulSoup(response.text, 'html.parser')

        authors_data.append({
            "fullname": soup.find('h3', class_='author-title').get_text().strip(),
            "born_date": soup.find('span', class_='author-born-date').get_text().strip(),
            "born_location": soup.find('span', class_='author-born-location').get_text().strip(),
            "description": soup.find('div', class_='author-description').get_text().strip()
        })  
    return authors_data


def main():
    quotes, links = get_quotes()
    authors = get_authors(links)

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=2)

    print("Скрапинг завершен. Файлы созданы.")

if __name__ == "__main__":
    main()