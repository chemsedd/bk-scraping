from scrapy.crawler import CrawlerProcess

from BookinSpider import BookingSpider
from config import SPIDER_SETTINGS, URL


def main():
    """
    Main function to start the Scrapy crawler for Booking.com
    """
    process = CrawlerProcess(SPIDER_SETTINGS)
    process.crawl(BookingSpider, start_url=URL)
    process.start()


if __name__ == "__main__":
    main()
