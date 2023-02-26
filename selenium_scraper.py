from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import re
import urllib.request

import requests
from bs4 import BeautifulSoup

# configure webdriver
options = Options()
options.headless = True  # hide GUI
# set window size to native GUI size
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")  # ensure window is full-screen

# Define input fields
search_phrase = "Climate Change"
news_category = "Science"
num_months = "2"
...
# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)
...

driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
#                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
driver.get("https://www.nytimes.com/")

search_field = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "query")))
search_field.send_keys(search_phrase)
search_field.submit()

# Apply filters to the search results
wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds

# Use more specific locators such as link text or id instead of xpath
wait.until(EC.presence_of_element_located((By.LINK_TEXT, f"{news_category}")))
driver.find_element(By.LINK_TEXT, f"{news_category}").click()

# Use driver.refresh() instead of driver.get() if possible
driver.refresh()

driver.quit()
