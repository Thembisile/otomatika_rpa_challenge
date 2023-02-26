import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send an HTTP GET request to the New York Times website
url = "https://www.nytimes.com/"
response = requests.get(url)
print("HTTP response status code:", response.status_code)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
print("Parsed HTML content:", soup)

# Extract the title and author of the first 5 articles
articles = []
for i, article in enumerate(soup.find_all("article")[:5]):
    title = article.find("h2").text.strip()
    author = article.find("span", {"class": "css-1n7hynb"}).text.strip()
    print(f"Article {i+1}: {title} by {author}")
    articles.append({"Title": title, "Author": author})

print("Extracted articles:", articles)

# Create a data frame and store the extracted data
df = pd.DataFrame(articles)

# Export the data frame to an excel file
df.to_excel("nyt_articles.xlsx", index=False)
print(f"Exported {len(articles)} articles to nyt_articles.xlsx")
