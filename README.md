Introduction

This is a Python script that allows you to search for news articles on the New York Times website using a **search phrase**, **category**, and number of **months** for which you need to receive news. The script uses the Selenium package to automate web browsing and Pandas package to store and analyze data.

Prerequisites

To be able to run the script, you will need to have the following installed on your system:

- Python 3.x
- pip package manager
- Installation

---

**Python: Python** is required to run the code. You can download the latest version of Python from the official website (https://www.python.org/downloads/) and install it on your system. The code should work with Python 3.7 or later.

**Chrome Browser**: The code uses the Chrome webdriver to automate the web browsing. Therefore, you need to have the Chrome browser installed on your system. You can download the latest version of Chrome from the official website (https://www.google.com/chrome/) and install it on your system.

**Chrome webdriver**: The code uses the Chrome webdriver to automate the web browsing. You need to download the Chrome webdriver that matches your Chrome browser version. You can download the Chrome webdriver from the official website (https://sites.google.com/a/chromium.org/chromedriver/downloads) and save it to your system. Make sure to add the path of the Chrome webdriver to the webdriver.chrome.driver environment variable.

**Required Python packages**: The code requires the pandas and selenium Python packages. You can install these packages using pip by running the following command:
```pip install pandas selenium```


Clone the repository or download the zip file and extract it.

```git clone -b master https://github.com/Thembisile/otomatika_rpa_challenge.git```

Open a terminal window and navigate to the project directory.

```cd otomatika*``` OR ```cd otomatika_rpa_challenge```

Install the required packages by running the following command:

```pip install -r requirements.txt```

Download the latest version of the Chrome driver compatible with your operating system from this link: 
[chromedriver download](https://sites.google.com/a/chromium.org/chromedriver/downloads). 

Extract the file and save the executable file in a location of your choice.

Open the ```nytimes.py``` file in a code editor of your choice and replace the value of the ```driver_path``` variable with the path of the Chrome driver executable file on your system.

## Running the script

Open a terminal window and navigate to the project directory.

Run the following command to start the script:

```python final_tester.py```

- Enter the search phrase when prompted.

- Select the news category from the options provided.

- Enter the number of months for which to receive news.

- Wait for the script to complete the search and extract the articles.

- The script will print the extracted articles in a Pandas DataFrame.
Conclusion

- This Python script provides an easy way to search for news articles on the New York Times website and extract information about them. With the help of the Selenium and Pandas packages, it automates web browsing and data storage and analysis.
