import requests
import search_para
import os
from dotenv import load_dotenv
load_dotenv()

# URL of the web page you want to access
url = 'https://apps.pcdirectory.gov.hk/Public/TC/AdvancedSearch?ProfID=RMP'
headers = {
	'User-Agent': 'Mozilla/5.0',
	'Content-Type': 'application/x-www-form-urlencoded',
	'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"macOS"',
	'Upgrade-Insecure-Requests': '1'
}
params = {'key': 'value'}


# Set up cookies
new_cookies = requests.cookies.RequestsCookieJar()
new_cookies['NET_SessionId'] = os.environ.get("NET_SessionId")
new_cookies['__RequestVerificationToken_L1B1YmxpYw2'] = os.environ.get("__RequestVerificationToken_L1B1YmxpYw2")

# Print cookies
for cookie in new_cookies:
    cookie_name = cookie.name
    cookie_value = cookie.value
    print(f"Cookie Name: {cookie_name}, Cookie Value: {cookie_value}")


# Import search parameters
para = search_para.search_para
para['__RequestVerificationToken'] = os.environ.get("__RequestVerificationToken")

url = 'https://apps.pcdirectory.gov.hk/Public/TC/AdvancedSearch'
# Sending POST request with the specified headers and data
response = requests.post(url, headers=headers, cookies=new_cookies, data=para)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open a file in binary write mode to save the response content
    with open('response.html', 'wb') as f:
        # Write the response content to the file
        f.write(response.content)
    print("Response saved as HTML file.")
else:
    print("Failed to retrieve response.")