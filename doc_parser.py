from bs4 import BeautifulSoup

def extract_doc_info(doc_counter):
    # Load HTML file
    with open(f'temp/doc_profile_{doc_counter}.html', 'r') as file:
        html_content = file.read()

    # Locate doc profile
    soup = BeautifulSoup(html_content, 'html.parser')
    doc_profile_div = soup.find('div', class_='Search-Box_container')
    doc_practice_div = doc_profile_div.find('div', class_='practice-detail-content')

    # Extract doc basic info
    doc_info = {}
    doc_name = doc_profile_div.find('div', class_='col-sm-9 Row-Padding').text.strip()
    doc_info["姓名"] = doc_name

    for legend_pair_div in doc_profile_div.findAll('div', class_='col-sm-6 Row-Padding'):
        legend = legend_pair_div.find('div', class_='col-12 legend').text.strip()
        info = legend_pair_div.find('div', class_='col-12 info').text.strip()
        doc_info[legend] = info


    

    for key, value in doc_info.items():
        print(key, ':', value)



    return None

extract_doc_info(1)
