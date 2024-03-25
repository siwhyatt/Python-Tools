# Get all link urls and text from a webpage

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

from dict_csv import dictToCSV
from sanitize_url import sanitize_url


def getLinks() -> list:
    url = sanitize_url(input("Url to scrape: "))
    links_clean = []

    with requests.session() as s:
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        try:
            response = s.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = bs(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return links_clean

    links_raw = soup.findAll('a', href=True)

    for link in links_raw:
        link_url = link['href']
        link_text = link.get_text(strip=True)
        link = {"url": link_url, "text": link_text}
        links_clean.append(link)

    pprint(links_clean)
    return links_clean

filename = "links.csv"
header = ["url", "text"]

def main():
    links_clean = getLinks()
    dictToCSV(filename, links_clean, header)


if __name__ == "__main__":
    main()