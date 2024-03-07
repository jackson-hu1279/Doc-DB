from bs4 import BeautifulSoup

BASE_URL = 'https://apps.pcdirectory.gov.hk'

def extract_doc_urls():
    # Load HTML file
    with open('temp/search_response.html', 'r') as file:
        html_content = file.read()

    # Locate all search results
    soup = BeautifulSoup(html_content, 'html.parser')
    search_result_div = soup.find(class_='SearchResult')
    result_items = search_result_div.find_all('div', class_='container mobile_SP_result')

    # Find doc name and link for each result item
    doc_url_lst = []
    counter = 0

    for single_result in result_items:
        doc_name = single_result.find(class_='col result-Doctor').text.strip()
        doc_link = single_result.find('a').get('href')
        full_doc_url = BASE_URL + doc_link
        doc_url_lst.append(full_doc_url)

        counter += 1
        print(f"({counter}) Found doc name: {doc_name}, link: {full_doc_url}")

    return doc_url_lst
