# Get all text from a webpage and create formatted google doc

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from sanitize_url import sanitize_url
from gdocs import gDocs


def getSoup():
    url = sanitize_url(input("Url to scrape: "))

    with requests.session() as s:
        s.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        try:
            response = s.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = bs(response.text, "html.parser")
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

def getText(soup) -> list:
    # List to hold the tag-text dictionaries
    elements_text = []
    
    # Iterate over all elements in the HTML document
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span']):  # `True` finds all tags
        if element.name and element.text:
            # Append a new dictionary with the tag name and its text content
            elements_text.append({element.name: element.text.strip()})
    
    return elements_text

def getTitle(soup) -> str:
    title = soup.find("h1")
    return title.text


def createDoc(title, elements_text):
    service = gDocs()
    body = {'title': title}
    doc = service.documents().create(body=body).execute()
    doc_id = doc.get('documentId')
    print(f'Created document titled "{title}" with ID: {doc_id}')

    requests = []
    index = 1

    # Insert document title as a big header
    requests.append({
        'insertText': {
            'location': {'index': index},
            'text': title + '\n'
        }
    })
    requests.append({
        'updateParagraphStyle': {
            'range': {
                'startIndex': index,
                'endIndex': index + len(title)
            },
            'paragraphStyle': {
                'namedStyleType': 'TITLE'
            },
            'fields': 'namedStyleType'
        }
    })
    index += len(title) + 1

    # Loop through each extracted text element and format according to its tag
    for element in elements_text:
        for tag, text in element.items():
            text += '\n'  # add a newline after each element for better readability
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': text
                }
            })

            # Define the style based on the tag
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                style = 'HEADING_' + tag[1:]
            else:
                style = 'NORMAL_TEXT'

            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': index,
                        'endIndex': index + len(text)
                    },
                    'paragraphStyle': {
                        'namedStyleType': style
                    },
                    'fields': 'namedStyleType'
                }
            })
            index += len(text)

    # Execute all formatting requests in a single batchUpdate call
    result = service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    print(f'Updated document with text and styles.')


def main():
    soup = getSoup()

    elements_text = getText(soup)

    title = getTitle(soup)

    createDoc(title, elements_text)

if __name__ == "__main__":
    main()