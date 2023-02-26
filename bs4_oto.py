import os
import datetime
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Read configuration variables from environment variables
search_phrase = "Climate Change"
news_category = "Science"
num_months = int("2")

# Calculate start and end dates based on number of months
today = datetime.date.today()
start_date = today - datetime.timedelta(days=num_months*30)
end_date = today - datetime.timedelta(days=1)

# Format start and end dates for use in URL
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Create URL for search results page
url = f"https://www.nytimes.com/search?endDate={end_date_str}&query={search_phrase}&sort=best&startDate={start_date_str}&section={news_category}"

# Send HTTP request to URL and parse response with BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Write headers to the worksheet
ws.append(["Title", "Link", "Published Date", "Summary"])

# Find all articles in the search results and extract relevant information
articles = soup.find_all("li", class_="css-1l4w6pd")
for article in articles:
    title = article.find("h4", class_="css-2fgx4k").text.strip()
    link = article.find("a", class_="css-1wjnrbv")["href"]
    published_date = article.find("time")["datetime"]
    summary = article.find("p", class_="css-1echdzn").text.strip()
    ws.append([title, link, published_date, summary])

# Save the workbook to a file
wb.save("nytimes_articles.xlsx")
