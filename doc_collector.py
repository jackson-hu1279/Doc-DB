import os
import sys
import pandas as pd
import requests
from dotenv import load_dotenv

from utils.search_para import search_para
from utils.search_parser import extract_doc_urls
from utils.doc_parser import extract_profile_info

load_dotenv()


# ==================================
#           Preparation
# ==================================


# Define IO paths and files
FILE_EXCHANGE_DIR = "input_output"
TEMP_DIR = "temp"
DOC_NAMES_EXCEL = "doc_names.xlsx"
OUTPUT_EXCEL = "doc_profile_result.xlsx"

# Bypass token verification
COOKIES = requests.cookies.RequestsCookieJar()
COOKIES['__RequestVerificationToken_L1B1YmxpYw2'] = os.environ.get(
    "__RequestVerificationToken_L1B1YmxpYw2")

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1'
}

def initialise():
    input_file_path = f"{FILE_EXCHANGE_DIR}/{DOC_NAMES_EXCEL}"
    output_file_path = f"{FILE_EXCHANGE_DIR}/{OUTPUT_EXCEL}"

    # Create directories for file exchange
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(FILE_EXCHANGE_DIR, exist_ok=True)

    return input_file_path, output_file_path


# ==================================
#      Get Match Search Results
# ==================================


def search_doc(doc_name):
    print("Doc to search:", doc_name)

    # Import search parameters
    request_para = search_para
    request_para['Name'] = doc_name
    request_para['__RequestVerificationToken'] = os.environ.get(
    "__RequestVerificationToken")

    # Sending POST request with the specified headers and data
    search_url = 'https://apps.pcdirectory.gov.hk/Public/TC/AdvancedSearch'
    search_response = requests.post(search_url, headers=HEADERS,
                            cookies=COOKIES, data=request_para)

    # Save if successfully get search reseults
    if search_response.status_code == 200:
        # Save search result conrent as HTML file
        with open('temp/search_response.html', 'wb') as f:
            f.write(search_response.content)
        print("Search results saved as HTML file.")
    else:
        print("Failed to retrieve search results.")

    # Extract doc profile urls
    print("\nParsing search results...")
    doc_url_lst = extract_doc_urls()

    return doc_url_lst


# ==================================
#    Extract Doc Profile Details
# ==================================


def extract_doc_detail(doc_url_lst):
    doc_profile_lst = []

    # Extract info from all profiles of a doc
    # Iterate through all search result URLs
    print("\nExtracting doc info from profile...")
    doc_counter = 0
    for doc_url in doc_url_lst:
        doc_counter += 1
        doc_profile_response = requests.get(doc_url, headers=HEADERS, cookies=COOKIES)

        print("\n" + "-" * 30 + "\n")
        print(f"Processing doc profile {doc_counter}")

        # Save doc profile as HTML
        if doc_profile_response.status_code == 200:
            with open(f'temp/doc_profile_{doc_counter}.html', 'wb') as f:
                f.write(doc_profile_response.content)
            print(f"Doc profile ({doc_counter}) saved as HTML file.")
        else:
            print(f"Failed to access doc profile {doc_url}")
            continue

        # Profile info extraction
        doc_profile_info = extract_profile_info(doc_counter)
        doc_profile_lst.append(doc_profile_info)
        
        # Info summary check (for debug)
        print("Required fields in doc profile extracted:\n")
        for key, value in doc_profile_info.items():
            print(key, ':', value)

    return doc_profile_lst


# ==================================
#          Clean Up Cache
# ==================================


def remove_temp_html(dir_name):
    for file in os.listdir(dir_name):
        # Delete only HTML files
        if file.endswith(".html"):
            file_path = os.path.join(dir_name, file)
            os.remove(file_path)

def cache_clean_up(dir_name):
    if os.path.exists(dir_name):
        # Remove any existing files
        for root, dirs, files in os.walk(dir_name, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
                
        # Remove directory itself
        os.rmdir(dir_name)


# ==================================
#          Driver Code
# ==================================
        

def main():
    # Preparation
    input_file_path, output_file_path = initialise()

    # Load input file & read given doc names
    if not os.path.exists(input_file_path):
        sys.exit(f"Error: Input file '{input_file_path}' does not exist!")

    input_df = pd.read_excel(input_file_path)
    doc_names = input_df['Name'].tolist()

    result_profiles = []    # Profile info collections

    # Iterate through given doc
    # Search & extract profile info
    for doc_name in doc_names:
        print("\n" + "=" * 30 + "\n")
        doc_url_lst = search_doc(doc_name)

        # Hande if no result found for name
        if len(doc_url_lst) == 0:
            print(f"Result not found for: {doc_name}")
            continue

        # Extract doc details from profile page
        doc_profile_lst = extract_doc_detail(doc_url_lst)
        for doc_profile in doc_profile_lst:
            doc_profile["Search Name"] = doc_name

        # Add current profile into collection
        result_profiles += doc_profile_lst

        # Clean up temp files
        remove_temp_html(TEMP_DIR)

    # Final clean up
    cache_clean_up(TEMP_DIR)

    # Organise collected profiles
    profile_fields = ["Search Name", "姓名", "性別", "電郵", "基層醫療服務提供者類別", "科別", "香港醫務委員會註冊號碼", "執業處所", "地址", "執業類別", "電話", "應診時間", "政府基層醫療促進計劃"]
    result_df = pd.DataFrame(result_profiles, columns=profile_fields)
    
    # Save doc detail results as an Excel file
    result_df.to_excel(output_file_path, index=False)


if __name__ == "__main__":
    main()