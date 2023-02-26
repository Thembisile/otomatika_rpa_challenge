import requests

# URL of the webpage to download
url = "https://www.nytimes.com/"

# Send a GET request to the URL to retrieve the HTML content
response = requests.get(url)

# Save the HTML content to a file using UTF-8 encoding
with open('NYT_Offline.html', 'w', encoding='utf-8') as file:
    file.write(response.text)
