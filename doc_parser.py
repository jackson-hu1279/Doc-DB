from bs4 import BeautifulSoup

def extract_table_content(table_div):
    table_data = ""

    # Iterate through each row in the table
    for row in table_div.find_all('tr'):
        row_data = ""
        # Iterate through each cell in the row
        for cell in row.find_all(['th', 'td']):
            row_data += cell.text.strip()
            
        table_data += (row_data + '\n')

    return table_data

def extract_doc_info(doc_counter):
    # Load HTML file
    with open(f'temp/doc_profile_{doc_counter}.html', 'r') as file:
        html_content = file.read()

    # Locate doc profile
    soup = BeautifulSoup(html_content, 'html.parser')
    doc_profile_div = soup.find('div', class_='Search-Box_container')
    doc_practice_div = doc_profile_div.find('div', class_='practice-detail-content')

    # Extract doc basic info
    profile_info = {}
    doc_name = doc_profile_div.find('div', class_='col-sm-9 Row-Padding').text.strip()
    profile_info["姓名"] = doc_name

    for legend_pair_div in doc_profile_div.findAll('div', class_='col-sm-6 Row-Padding'):
        legend = legend_pair_div.find('div', class_='col-12 legend').text.strip()
        info = legend_pair_div.find('div', class_='col-12 info').text.strip()
        profile_info[legend] = info

    # Extract doc practice info
    required_fields = ["地址", "執業類別", "電話", "應診時間", "政府基層醫療促進計劃"]
    current_pracice_div = doc_practice_div.find('div', id='lst001')
    for legend_pair_div in current_pracice_div.findAll('div', class_='content-section'):
        legend = legend_pair_div.find('div', class_='legend').text.strip()

        # Skip unnecessary fields
        if legend not in required_fields:
            continue

        info = legend_pair_div.find('div', class_='info').text.strip()

        if legend == "應診時間":
            table_data = extract_table_content(legend_pair_div.find('table'))
            info = table_data

        if legend == "政府基層醫療促進計劃":
            plan = []
            if "CRCSP" in info:
                print("CRSCP True")
                plan.append("CRCSP")
            if "HCVS" in info:
                print("HCVS True")
                plan.append("HCVS")
            info = str(plan)
        print(legend, info)

    
    

    # for key, value in profile_info.items():
    #     print(key, ':', value)



    return None

extract_doc_info(1)
