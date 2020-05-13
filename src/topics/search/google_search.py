import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .search import Search

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class GoogleSearch(Search):
    def __init__(self):
        super().__init__(engine="google")

    def search_engine(self, query):
        try:
            q = self.parse_google_command(query)
            logger.info(f"JAZZ: Querying Google for {q}")

            browser = webdriver.Chrome()
            browser.get("http://www.google.com")
            search = browser.find_element_by_name("q")
            search.send_keys(q)
            search.send_keys(Keys.RETURN)

            # Wait for the whole google page to load
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "result-stats")))

            # get all URLs
            links = browser.find_elements_by_xpath("//*[@id='rso']/*[@class='g']//*[@class='r']//a")
            urls = [link.get_attribute("href") for link in links]

            # Open max_tab_count tabs
            self.open_urls(browser, urls)
        except Exception as e:
            logger.error(f"ERROR: {e}")

    def parse_google_command(self, command):
        answer = command
        for word in self.stopwords:
            answer = answer.replace(word, "")
        return answer

    def open_urls(self, browser, urls):
        link_counter = 0

        for url in set(urls):
            # Don't open more than max_tab_count # of tabs
            if link_counter >= self.max_tab_count:
                break

            # Clean URL check - don't want cached pages
            if ("google.com" not in url) and ("webcache.googleusercontent.com" not in url):
                # open new blank tab
                browser.execute_script("window.open();")
                time.sleep(0.02)

                # switch to the new window which is second in window_handles array
                browser.switch_to_window(browser.window_handles[-1])

                browser.get(url)
                link_counter += 1

        logger.info(f"JAZZ: Opened {link_counter} tabs")
