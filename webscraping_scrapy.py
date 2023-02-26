import scrapy

class NYTimesSpider(scrapy.Spider):
    name = "nytimes"
    start_urls = ["https://www.nytimes.com/search?query=Climate"]

    def parse(self, response):
        # Apply filters to the search results page
        # Select news category or section
        # Choose the latest news
        # Extract data from the filtered results page
        for article in response.css("article"):
            title = article.css("h4 > a::text").get()
            date = article.css("span[itemprop=datePublished]::text").get()
            description = article.css("p::text").get()
            picture_url = article.css("img::attr(src)").get()

            # Count search phrase occurrences in title and description
            search_phrase_count = 0
            if title:
                search_phrase_count += title.count("Climate Change")
            if description:
                search_phrase_count += description.count("Climate Change")

            # Check if title or description contains any amount of money
            has_money = False
            if title:
                if "$" in title or "dollar" in title.lower() or "usd" in title.lower():
                    has_money = True
            if description:
                if "$" in description or "dollar" in description.lower() or "usd" in description.lower():
                    has_money = True

            # Create an item to store the scraped data
            item = {
                "title": title,
                "date": date,
                "description": description,
                "picture_url": picture_url,
                "search_phrase_count": search_phrase_count,
                "has_money": has_money
            }
            yield item
