from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import urllib
from urllib.parse import urlparse
from urllib.request import urlretrieve
import os


def get_news_data(
    search_phrase: str,
    news_category: str,
    num_of_months: int,
    results: List[Dict[str, Any]],
    page_num: int = 1,
    max_page_num: int = None,
) -> List[Dict[str, Any]]:
    # Set up base URL
    url = "https://www.nytimes.com/search?"

    # Set up search query parameters
    search_params = {
        "query": search_phrase,
        "sort": "newest",
        "page": page_num,
    }
    print("Search parameters:", search_params)
    print("URL:", url + urllib.parse.urlencode(search_params))
    # Set up news category filter
    if news_category:
        search_params["sections"] = news_category

    # Set up date filter
    today = datetime.today()
    start_date = today.replace(day=1)
    end_date = start_date - timedelta(days=1)
    for _ in range(num_of_months):
        start_date = end_date.replace(day=1)
        end_date = start_date - timedelta(days=1)
    search_params["begin_date"] = start_date.strftime("%Y%m%d")
    search_params["end_date"] = end_date.strftime("%Y%m%d")

    # Make HTTP request
    response = requests.get(url, params=search_params)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract news data
    articles = soup.find_all("li", class_="css-1l4w6pd")
    print(f"Found {len(articles)} articles.")
    if not articles:
        print("No results found.")
    else:
        print("Found", len(articles), "articles.")
        for article in articles:
            title_elem = article.find("h4")
            if not title_elem:
                continue
            title = title_elem.text.strip()

            summary_elem = article.find("p", class_="css-1echdzn")
            summary = summary_elem.text.strip() if summary_elem else ""

            date_elem = article.find("time")
            date = date_elem["datetime"] if date_elem else ""

            img_elem = article.find("img")
            img_url = img_elem["src"] if img_elem else ""
            if img_url:
                img_url = "https://www.nytimes.com" + img_url
                filename = os.path.basename(urlparse(img_url).path)
                urlretrieve(img_url, filename)

        # Extract money value
        has_money = False
        money_regex = r"\$\d+(?:,\d+)?(?:\.\d+)?\b|\d+(?:,\d+)?\s+dollar[s]?"
        if re.search(money_regex, title) or re.search(money_regex, summary):
            has_money = True

        # Extract search phrase count
        search_phrase_count = title.count(
            search_phrase) + summary.count(search_phrase)

        # Store news data
        news_data = {
            "title": title,
            "date": date,
            "description": summary,
            "picture filename": filename,
            "count of search phrases": search_phrase_count,
            "has money": has_money,
            "search phrase count": search_phrase_count
        }

        print(f"Adding news data: {news_data}")
        results.append(news_data)
       # Recursively call function to scrape next page
    if max_page_num is None or page_num < max_page_num:
        get_news_data(
            search_phrase,
            news_category,
            num_of_months,
            results,
            page_num + 1,
            max_page_num,
        )

    return results


# Extract news data
results = get_news_data("Climate Change", "Science", 12, [], max_page_num=2)
print(results)

# Write data to Excel file
wb = Workbook()
ws = wb.active
ws.append(["Title", "Date", "Description", "Picture Filename", "Count of Search Phrases", "Has Money"])
for result in results:
    ws.append([
        result["title"],
        result["date"],
        result["description"],
        result["picture filename"],
        result["count of search phrases"],
        result["has money"],
        result["search phrase count"]
    ])
wb.save("nytimes_news.xlsx")
