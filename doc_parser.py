from bs4 import BeautifulSoup

# Extract practice address
def extract_practice_addrss(doc_practice_div):
    map_div = doc_practice_div.find('div', class_='map')
    address = map_div.find('div', class_='info').text.strip()
    return address

# Extract opening hours info from table
def extract_table_content(table_div):
    table_data = ""

    # Iterate through each row in the table
    for row in table_div.children:
        # Locate level 1 row elements
        if row.name == 'tr':
            row_data = ""
            day = row.find('td').text.strip()
            time_range = row.find('table').text.strip()

            # Organise data format for a single day
            row_data += (day + '' + time_range)
            table_data += (row_data + '\n')

    return table_data.strip()

# Extract care program info
def extract_care_program(program_div):
    programs = []

    for entry in program_div.find_all('a'):
        programs.append(entry.text.strip())

    return programs

# Get current practice tab
def get_current_practice_ref(page_content):
    practice_ref = page_content.find('a', class_='active').get('href')
    practice_ref = practice_ref.replace("#", "")

    return practice_ref

# Extract required doc info (main logic)
def extract_doc_info(doc_counter):
    # Load HTML file
    with open(f'temp/doc_profile_{doc_counter}.html', 'r') as file:
        html_content = file.read()

    # Locate doc profile
    soup = BeautifulSoup(html_content, 'html.parser')
    doc_profile_div = soup.find('div', class_='Search-Box_container')
    doc_practice_div = doc_profile_div.find('div', class_='practice-detail-content')
    practice_ref = get_current_practice_ref(soup)

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
    current_pracice_div = doc_practice_div.find('div', id=practice_ref)
    for legend_pair_div in current_pracice_div.findAll('div', class_='content-section'):
        legend = legend_pair_div.find('div', class_='legend').text.strip()

        # Skip unnecessary fields
        if legend not in required_fields:
            continue

        # Extract info based on fields
        if legend == "地址":
            practice_name = legend_pair_div.find('div', class_='info').text.strip()
            practice_address = extract_practice_addrss(doc_practice_div)
            profile_info["執業處所"] = practice_name
            profile_info["地址"] = practice_address
        elif legend == "應診時間":
            table_data = extract_table_content(legend_pair_div.find('table'))
            profile_info["應診時間"] = table_data
        elif legend == "政府基層醫療促進計劃":
            programs = extract_care_program(legend_pair_div.find('table'))
            profile_info["政府基層醫療促進計劃"] = ', '.join(programs)
        else:
            info = legend_pair_div.find('div', class_='info').text.strip()
            profile_info[legend] = info
        
    
    # Info summary check (for debug)
    for key, value in profile_info.items():
        print(key, ':', value)

    return profile_info

extract_doc_info(2)

