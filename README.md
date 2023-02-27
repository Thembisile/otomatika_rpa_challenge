Introduction

This is a Python script that allows you to search for news articles on the New York Times website using a **search phrase**, **category**, and number of **months** for which you need to receive news. The script uses the Selenium package to automate web browsing and Pandas package to store and analyze data.

Prerequisites

To be able to run the script, you will need to have the following installed on your system:

- Python 3.x
- pip package manager
- Installation

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

```python nytimes.py```

- Enter the search phrase when prompted.

- Select the news category from the options provided.

- Enter the number of months for which to receive news.

- Wait for the script to complete the search and extract the articles.

- The script will print the extracted articles in a Pandas DataFrame.
Conclusion

- This Python script provides an easy way to search for news articles on the New York Times website and extract information about them. With the help of the Selenium and Pandas packages, it automates web browsing and data storage and analysis.
