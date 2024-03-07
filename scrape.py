import requests
import search_para
import os
from dotenv import load_dotenv
load_dotenv()


# ==============
# Search Name
# ==============


# Set name of doc to find
doc_name = "CHAN KAI MING"

# Import search parameters
request_para = search_para.search_para
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
response = requests.post(search_url, headers=headers,
                         cookies=cookies, data=request_para)

# Save if successfully get search reseults
if response.status_code == 200:
    # Save search result conrent as HTML file
    with open('response.html', 'wb') as f:
        f.write(response.content)
    print("Response saved as HTML file.")
else:
    print("Failed to retrieve response.")
