import requests
import os
from dotenv import load_dotenv

from search_para import search_para
from search_parser import extract_doc_urls
from doc_parser import extract_profile_info

load_dotenv()


# ======================
# Search Doc Name
# ======================


# Set name of doc to find
doc_name = "CHAN KAI MING"
print("Doc to search:", doc_name)

# Import search parameters
request_para = search_para
request_para['Name'] = doc_name

# Bypass token verification
cookies = requests.cookies.RequestsCookieJar()
cookies['__RequestVerificationToken_L1B1YmxpYw2'] = os.environ.get(
    "__RequestVerificationToken_L1B1YmxpYw2")
request_para['__RequestVerificationToken'] = os.environ.get(
    "__RequestVerificationToken")

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1'
}

# Sending POST request with the specified headers and data
search_url = 'https://apps.pcdirectory.gov.hk/Public/TC/AdvancedSearch'
search_response = requests.post(search_url, headers=headers,
                         cookies=cookies, data=request_para)

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


# ======================
# Extract Doc Profile
# ======================


print("\nExtracting doc info from profile...")
doc_counter = 0
for doc_url in doc_url_lst:
    doc_counter += 1
    doc_profile_response = requests.get(doc_url, headers=headers, cookies=cookies)

    print(f"\nProcessing doc profile {doc_counter}")

    # Save doc profile as HTML
    if doc_profile_response.status_code == 200:
        with open(f'temp/doc_profile_{doc_counter}.html', 'wb') as f:
            f.write(doc_profile_response.content)
        print(f"Doc profile ({doc_counter}) saved as HTML file.")
    else:
        print(f"Failed to access doc profile {doc_url}")
        continue

    doc_profile_info = extract_profile_info(doc_counter)
    # Info summary check (for debug)
    print("Required fields in doc profile extracted:\n")
    for key, value in doc_profile_info.items():
        print(key, ':', value)