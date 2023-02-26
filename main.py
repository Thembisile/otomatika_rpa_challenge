from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import re
import urllib.request

# Set up the Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Define input fields
search_phrase = "Climate Change"
news_category = "Science"
num_months = "2"

# Navigate to the nytimes.com website
driver.get("https://www.nytimes.com/")

# Enter the search phrase in the search field and submit the form
search_field = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "query")))
search_field.send_keys(search_phrase)
search_field.submit()

# Apply filters to the search results
wait = WebDriverWait(driver, 10) # wait for up to 10 seconds

# Use more specific locators such as link text or id instead of xpath
wait.until(EC.presence_of_element_located((By.LINK_TEXT, f"{news_category}")))
driver.find_element(By.LINK_TEXT,f"{news_category}").click()

# Use driver.refresh() instead of driver.get() if possible
driver.refresh()

# Use Linq queries to filter elements by attributes
# addButtons = driver.find_elements(By.TAG_NAME, "a")


# Extract information from each news article
wb = openpyxl.Workbook()
ws = wb.active
ws.append(["Title", "Date", "Description", "Picture Filename",
          "Count of Search Phrases", "Contains Money Amount"])
for month in range(int(num_months)):
    # Extract the title, date, and description of each news article
    articles = driver.find_elements_by_xpath(
        "//ol[@data-testid='search-results']//li")
    for article in articles:
        title_elem = article.find_element_by_xpath(".//h4/a")
        title = title_elem.text
        date_elem = article.find_element_by_xpath(".//time")
        date = date_elem.get_attribute("datetime")
        description_elem = article.find_element_by_xpath(
            ".//p[@class='css-1echdzn evys1bk0']")
        description = description_elem.text

        # Determine if the title or description contains the search phrase
        search_phrase_count = len(re.findall(
            search_phrase, f"{title} {description}", re.IGNORECASE))

        # Determine if the title

        contains_money = "False"
        if re.search(r"\$[\d,]+(\.\d{2})?\b|\b\d+ dollars?\b|\b\d+ USD\b", f"{title} {description}"):
            contains_money = "True"

        # Write the extracted information to the Excel worksheet
        ws.append([title, date, description, "",
                  search_phrase_count, contains_money])

        # Download the picture associated with the news article and add its filename to the worksheet
        # TODO: Add code for downloading pictures and adding their filenames to the worksheet

    # Navigate to the next month's search results
    driver.get(
        f"https://www.nytimes.com/search?endDate={date}&query={search_phrase}&sort=best&startDate={date}")

# Save the Excel workbook
wb.save("nytimes_articles.xlsx")

# Quit the Selenium driver
driver.quit()
