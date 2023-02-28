import time
import pandas as pd
from RPA.Browser.Selenium import Selenium

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

# Set up the Selenium browser
browser = Selenium()
browser.open_available_browser()

# Define a function to navigate to the search page
def navigate_to_search_page():
    browser.go_to('https://www.nytimes.com/search')
    browser.wait_until_page_contains_element('//*[@id="search-input"]')
    search_input = browser.get_webelement('//*[@id="search-input"]')
    search_input.send_keys(search_phrase)
    search_button = browser.get_webelement('//*[@id="search-button"]')
    search_button.click()

    # Wait for the filters to load and then select the news category
    time.sleep(5)
    filters = browser.get_webelement('//*[@class="search-filters"]')
    category_dropdown = filters.find_element_by_class_name('category-dropdown')
    category_dropdown.click()
    category_options = category_dropdown.find_elements_by_tag_name('option')
    for option in category_options:
        if option.text.lower() == news_category.lower():
            option.click()
            break

    # Select the latest news
    time.sleep(5)
    sort_dropdown = filters.find_element_by_class_name('sort-dropdown')
    sort_dropdown.click()
    sort_options = sort_dropdown.find_elements_by_tag_name('option')
    for option in sort_options:
        if option.text.lower() == "newest":
            option.click()
            break
