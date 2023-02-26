import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd
import os

# Define the search phrase, news category or section, and number of months
search_phrase = "climate change"
news_category = "science"
num_of_months = 1

# Set the base URL and headers for requests
base_url = "https://www.nytimes.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# Define a function to get the latest news URL for the given search phrase and news category


def get_latest_news_url(search_phrase, news_category):
    search_url = f"{base_url}search?q={search_phrase}&sort=newest"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("li", class_="css-1l4w6pd")
    for article in articles:
        try:
            category = article.find("a", class_="css-1ghb62w").text.lower()
            if news_category.lower() in category:
                return article.find("a")["href"]
        except:
            pass
    return None

# Define a function to get the article details from the given URL


def get_article_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title = soup.find("h1").text.strip()
    except:
        title = None
    try:
        date = soup.find("time")["datetime"][:10]
    except:
        date = None
    try:
        description = soup.find("p", class_="css-axufdj evys1bk0").text.strip()
    except:
        description = None
    try:
        img_url = soup.find("figure").find("img")["src"]
    except:
        img_url = None
    return title, date, description, img_url

# Define a function to check if a given text contains any amount of money


def contains_money(text):
    pattern = r"\$[\d,.]+|\d+ (dollars|USD)"
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False

# Define a function to scrape the news for the given search phrase, news category, and number of months


def scrape_news(search_phrase, news_category, num_of_months):
    # Set up the output dataframe
    columns = ["Title", "Date", "Description", "Picture Filename",
               "Search Phrase Count", "Contains Money"]
    data = []
    df = pd.DataFrame(data, columns=columns)

    # Calculate the date range for the given number of months
    today = datetime.date.today()
    num_of_days = num_of_months * 30
    start_date = today - datetime.timedelta(days=num_of_days)

    # Get the latest news URL for the given search phrase and news category
    url = get_latest_news_url(search_phrase, news_category)
    if url:
        # Get the article details from the URL
        title, date, description, img_url = get_article_details(url)
        if title and date:
            # Check if the article date is within the date range
            article_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            if article_date >= start_date and article_date <= today:
                # Check if the article contains the search phrase
                title_count = title.lower().count(search_phrase.lower())
                if description:
                    desc_count = description.lower().count(search_phrase.lower())
                else:
                    desc_count = 0
                # Check if the article contains any amount of money
                has_money = contains_money(
                    title) or contains_money(description)
                # Download the image and save it with a unique filename
                if img_url:
                    response = requests.get(img_url, headers=headers)
                    if response.status_code == 200:
                        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
                        with open(filename, "wb") as f:
                            f.write(response.content)
                else:
                    filename = None
                # Add the article details to the output dataframe
                row = [title, date, description, filename,
                       title_count+desc_count, has_money]
                df.loc[len(df)] = row


    # Save the output dataframe to an Excel file
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = f"output/{search_phrase}_{news_category}_{num_of_months}m.xlsx"
    print(filename)
    df.to_excel(filename, index=False)
    
scrape_news("climate change", "science", 1)