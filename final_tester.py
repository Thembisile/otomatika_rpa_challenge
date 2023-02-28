import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from RPA.Browser.Selenium import Selenium


# Prompt the user to enter the search phrase
search_phrase = input("Enter the search phrase: ")

# Prompt the user to select a news category from a dropdown
category_options = ["Arts", "Automobiles", "Books", "Business", "Fashion", "Food", "Health", "Home",
                    "Insider", "Magazine", "Movies", "NYRegion", "Obituaries", "Opinion", "Politics",
                    "RealEstate", "Science", "Sports", "SundayReview", "Technology", "Theater",
                    "T-magazine", "Travel", "Upshot", "US", "World"]
print("Select a news category:")
for i, category in enumerate(category_options):
    print(f"{i+1}. {category}")
category_index = int(input("Enter the number of the category: ")) - 1
news_category = category_options[category_index]

# Prompt the user to enter the number of months for which to receive news
num_months = int(
    input("Enter the number of months for which you need to receive news: "))

# Set up the Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Define a function to set up the driver and navigate to the search page
def navigate_to_search_page():
    driver.get("https://www.nytimes.com/search")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "css-1j26cud")))
    search_input = driver.find_element(
        By.CSS_SELECTOR, By.CSS_SELECTOR, "css-1j26cud")
    search_input.send_keys(search_phrase)
    search_button = driver.find_element(By.CSS_SELECTOR, "css-1gudca6")
    search_button.click()

    # Wait for the filters to load and then select the news category
    time.sleep(5)
    filters = driver.find_element(By.CLASS_NAME, "search-filters")
    category_dropdown = filters.find_element(
        By.CLASS_NAME, "category-dropdown")
    category_dropdown.click()
    category_options = category_dropdown.find_elements(By.TAG_NAME, "option")
    for option in category_options:
        if option.text.lower() == news_category.lower():
            option.click()
            break

    # Select the latest news
    time.sleep(5)
    sort_dropdown = filters.find_element(By.CLASS_NAME, "sort-dropdown")
    sort_dropdown.click()
    sort_options = sort_dropdown.find_elements(By.TAG_NAME, "option")
    for option in sort_options:
        if option.text.lower() == "newest":
            option.click()
            break

# Define a function to extract the articles
def extract_articles():
    articles = []
    search_results = driver.find_elements(By.CLASS_NAME, "query")
    for i, result in enumerate(search_results):
        # Check if the article was published within the specified timeframe
        time_element = result.find_element(By.CLASS_NAME, "css-1echdzn")
        article_date = pd.to_datetime(time_element.get_attribute("datetime"))
        if article_date < pd.Timestamp.now() - pd.DateOffset(months=num_months):
            continue

            # Extract the title, description, and picture filename
        title_element = result.find_element(By.CLASS_NAME, "css-1echdzn")
        title = title_element.text.strip()
        desc_element = result.find_element(By.CLASS_NAME, "css-1nynj0h")
        description = desc_element.text.strip()
        try:
            picture_element = result.find_element(By.TAG_NAME, "img")
            picture_filename = picture_element.get_attribute("src")
        except:
            picture_filename = ""

        # Extract the article link
        link_element = result.find_element(By.TAG_NAME, "a")
        article_link = link_element.get_attribute("href")

        # Append the article information to the articles list
        articles.append({
            "Title": title,
            "Description": description,
            "Picture Filename": picture_filename,
            "Link": article_link
        })
    return articles


navigate_to_search_page()

articles = extract_articles()

driver.quit()
df = pd.DataFrame(articles)
print(df.head())
