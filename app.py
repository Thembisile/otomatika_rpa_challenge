from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import openpyxl
from openpyxl import Workbook
import os
import urllib, urllib3

# Set up the Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Define the search phrase, news category, and number of months
search_phrase = "Climate Change" # Enter the search phrase here
news_category = "Science" # Enter the news category or section here
num_of_months = 2 # Enter the number of months for which you need to receive news here

# Initialize the Chrome webdriver and navigate to the site
driver = webdriver.Chrome(options=options)
driver.get("https://www.nytimes.com/")

# Find the search field and enter the search phrase
search_field = driver.find_element(By.CSS_SELECTOR, ("input[data-testid='search-input']"))
search_field.send_keys(search_phrase)
search_field.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(3)

# Find and click the "Sort by" button to sort by latest news
sort_button = driver.find_element(By.XPATH, "//button[contains(@class, 'popup-visible css-4d08fs')]")
sort_button.click()
time.sleep(1)
latest_news_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Latest')]")
latest_news_button.click()

# Find and click the news category button
category_button = driver.find_element(By.XPATH, "//button[@data-testid='search-filters-menu-button']")
category_button.click()
time.sleep(1)

# Find and select the news category
category_option = driver.find_element(By.XPATH, f"//a[contains(text(), '{news_category}')]")
category_option.click()

# Wait for the search results to load
time.sleep(3)

# Initialize the workbook and worksheet for storing the data
wb = Workbook()
ws = wb.active
ws.append(["Title", "Date", "Description", "Picture Filename", "Search Phrase Count", "Contains Money?"])

# Find and loop through the search result items
result_items = driver.find_elements(By.XPATH, "//li[contains(@data-testid, 'search-bodega-result')]")
for item in result_items:
    # Find the title and date of the news article
    title = item.find_element(By.XPATH, ".//h4").text
    date = item.find_element(By.XPATH, ".//time").get_attribute("datetime")
    
    # Find the link to the news article and navigate to it
    link = item.find_element(By.XPATH, ".//a").get_attribute("href")
    driver.get(link)
    
    # Find and get the description of the news article, if available
    try:
        description = driver.find_element(By.XPATH, "//p[contains(@class, 'css-')][1]")
        description = description.text
    except:
        description = ""
    
    # Find and download the news picture
    try:
        picture = driver.find_element(By.XPATH, "//figure[@class='css-0']")
        picture_url = picture.find_element(By.XPATH, ".//img").get_attribute("src")
        picture_filename = f"{title}.jpg"
        urllib.request.urlretrieve(picture_url, picture_filename)
    except:
        picture_filename = ""
    
    # Count the number of times the search phrase appears in the title and description
    search_phrase_count = title.count(search_phrase)
    search_phrase_count += description.count(search_phrase)
    
    # Check if the title or description contains any amount of

    contains_money = False # Enter your code here to check if the title or description contains any amount of money
    
    # Add the data to the worksheet
    ws.append([title, date, description, picture_filename, search_phrase_count, contains_money])
    
# Save the workbook and close the Chrome webdriver
wb.save("nytimes_news_shaun.xlsx")