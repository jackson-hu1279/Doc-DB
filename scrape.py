import requests

# URL of the web page you want to access
url = 'https://apps.pcdirectory.gov.hk/Public/TC/AdvancedSearch?ProfID=RMP'
headers = {
	'User-Agent': 'Mozilla/5.0'
}
params = {'key': 'value'}

response = requests.get(url, headers=headers, params=params)

# Get the cookies from the response
cookies = response.cookies

# Print the cookies
for cookie in cookies:
    cookie_name = cookie.name
    cookie_value = cookie.value
    print(f"Cookie Name: {cookie_name}, Cookie Value: {cookie_value}")