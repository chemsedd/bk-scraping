import json
import time

import scrapy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BookingSpider(scrapy.Spider):
    name = "booking_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        """
        Initialize the BookingSpider with a start URL and Selenium WebDriver settings.
        """
        super(BookingSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

        # load more button selector
        self.load_more_selector = (
            ".de576f5064.b46cd7aad7.d0a01e3d83.dda427e6b5.bbf83acb81.a0ddd706cc"
        )
        # listing item selector
        self.item_selector = "[data-testid='property-card-container']"
        # Time to wait after scrolling
        self.scroll_pause_time = 2
        # Time to wait after clicking load more button
        self.click_wait_time = 3
        # Maximum number of scroll attempts
        self.max_scroll_attempts = 50

        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Remove for debugging
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        # Keep track of processed items
        self.processed_items = set()
        # Current batch of scraped items
        self.current_batch = []
        # Final data to be saved
        self.final_data = []

    def start_requests(self):
        """
        Start requests for the spider
        """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Main parsing method that handles scrolling and clicking
        """
        self.driver.get(response.url)

        # Wait for initial page load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        scroll_attempts = 0

        while scroll_attempts < self.max_scroll_attempts:
            self.scroll_to_bottom()
            self.process_visible_items()

            # Check if load more button exists and click it
            if self.click_load_more_button():
                self.logger.info(
                    f"Clicked load more button, attempt {scroll_attempts + 1}"
                )
                time.sleep(self.click_wait_time)
                scroll_attempts += 1
            else:
                self.logger.info("No more load more buttons found, finishing scraping")
                break

        # Process any remaining items in the final batch
        self.process_final_batch()
        # Save final data to file output.jsonl
        self.save_data()

        # Close the driver
        self.driver.quit()

    def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page
        """

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait for new content to load
            time.sleep(self.scroll_pause_time)

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def click_load_more_button(self):
        """
        Check if load more button exists and click it
        """

        try:
            load_more_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.load_more_selector))
            )

            # Scroll to the button to ensure it's visible
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", load_more_button
            )
            time.sleep(1)

            # Click the button
            load_more_button.click()
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def process_visible_items(self):
        """
        Process currently visible items and manage memory
        """

        try:
            # Get all items currently visible on page
            items = self.driver.find_elements(By.CSS_SELECTOR, self.item_selector)

            for item in items:
                # Create unique identifier for the item
                item_id = self.get_item_id(item)

                # Skip if already processed
                if item_id in self.processed_items:
                    continue

                # Extract data from item
                item_data = self.extract_item_data(item)
                if item_data:
                    self.current_batch.append(item_data)
                    self.processed_items.add(item_id)
                    self.final_data.append(item_data)

            # Clean up processed items from DOM to save memory
            self.cleanup_processed_items()

        except Exception as e:
            self.logger.error(f"Error processing items: {e}")

    def get_item_id(self, item):
        """
        Generate unique ID for an item
        """

        try:
            item_id = item.get_attribute("data-id")
            if not item_id:
                text_content = item.text[:100]
                item_id = str(hash(text_content))
            return item_id
        except Exception:
            return str(hash(item.get_attribute("outerHTML")[:100]))

    def extract_item_data(self, item):
        """
        Extract data from a single item
        """

        try:
            title = item.find_element(By.CSS_SELECTOR, "[data-testid='title']").text
            score = item.find_element(
                By.CSS_SELECTOR, "[data-testid='review-score'] > div:nth-child(2)"
            ).text

            return {
                "title": title,
                "score": score,
            }
        except Exception as e:
            self.logger.debug(f"Error extracting item data: {e}")
            return {}

    def process_final_batch(self):
        """
        Process any remaining items in the final batch
        """
        if self.current_batch:
            for item_data in self.current_batch:
                yield item_data
            self.logger.info(
                f"Processed final batch of {len(self.current_batch)} items"
            )

    def cleanup_processed_items(self):
        """
        Remove processed items from DOM to save memory
        """

        try:
            # Remove processed items from DOM
            self.logger.debug("Cleaning up processed items from DOM...")
            self.driver.execute_script(
                """
                var items = document.querySelectorAll("[data-testid='property-card']");
                var toRemove = [];
                for (var i = 0; i < items.length - 1; i++) {  
                    toRemove.push(items[i]);
                }
                toRemove.forEach(function(item) {
                    item.remove();
                });""",
                self.item_selector,
            )

        except Exception as e:
            self.logger.debug(f"Error during cleanup: {e}")

    def save_data(self):
        """
        Save final data to a file
        """

        with open("output.jsonl", "w", encoding="utf-8") as f:
            for item_data in self.final_data:
                f.write(json.dumps(item_data, ensure_ascii=False) + ",\n")
        self.logger.info(f"Saved {len(self.final_data)} items to output.jsonl")

    def closed(self, reason):
        """
        Clean up when spider closes
        """

        try:
            self.driver.quit()
        except Exception:
            pass
        self.logger.info(f"Spider closed: {reason}")
