import logging
import sys
from abc import ABC, abstractmethod

import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
from selenium import webdriver


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class Search(ABC):
    def __init__(self, engine=""):
        self.max_tab_count = 1
        self.stopwords = self.__cache_stopwords(engine)
        super().__init__()

    def __cache_stopwords(self, engine):
        cached_stopwords = stopwords.words("english")
        cached_exceptions = [f"{word} {engine}" for word in cached_stopwords]
        cached_exceptions += [f"{engine} {word}" for word in cached_stopwords]
        return cached_exceptions

    @abstractmethod
    def search_engine(self, query):
        """
        Uses this function to search the search engine with the given query
        Opens up G Chrome with the search
        """
        try:
            logger.info(f"JAZZ: Searching the internet for {query}")
            updated_query = query.replace(" ", "+")
            url = f"http://www.google.com/search?q={updated_query}"
            browser = webdriver.Chrome()
            browser.get(url)
        except Exception as e:
            logger.error(f"ERROR: {e}")


# #


#     def parse_google_command(command):
#         answer = command
#         for word in cached_exceptions:
#             answer = answer.replace(word, "")
#         return answer

#     def search_engine(self, query):
#         try:
#             self.browser.get('http://www.google.com')
#             search = browser.find_element_by_name('q')
#             search.send_keys(query)
#             search.send_keys(Keys.RETURN)

#             # Wait for the whole google page to load
#             WebDriverWait(browser, 10).until(
#                 EC.visibility_of_element_located((By.ID, "result-stats")))

#             # get all URLs
#             links = browser.find_elements_by_xpath("//*[@id='rso']/*[@class='g']//*[@class='r']//a")
#             urls = [link.get_attribute('href') for link in links]


#     def open_urls(self, urls):
#         link_counter = 0

#         for url in set(urls):
#             # Don't open more than max_tab_count # of tabs
#             if link_counter >= self.max_tab_count:
#                 break

#             # Clean URL check - don't want cached pages
#             if ('google.com' not in url) and ('webcache.googleusercontent.com' not in url):
#                 # open new blank tab
#                 browser.execute_script("window.open();")
#                 time.sleep(0.05)

#                 # switch to the new window which is second in window_handles array
#                 browser.switch_to_window(browser.window_handles[-1])

#                 browser.get(url)
#                 link_counter += 1


#     def search_category(self, command):
#         sub_command = remove_word_from_command("search", command)
#         if 'google' in sub_command:
#             query = parse_google_command(sub_command)
#             self.search_google(query)
#             # query = remove_stopwords(query)
#             print(query)
#         # if reg_ex:
#         #     topic = reg_ex.group(1)
#         # if 'google' in topic:
#         #     reg_ex = re.search(' (.*) google', command)
#         #     print(reg_ex)
#         #     if reg_ex:
#         #         topic = reg_ex.group(1)
#     #         search_google(topic)
#     #     elif 'mac' or 'macbook' in command:
#     #         search_mac()
#     #     elif 'stack overflow' or 'stackoverflow' in command:
#     #         search_stack_overflow()
#     #     else:
#     #         search_google()


#     def search_google(self, query):
#         try:
#             browser.get('http://www.google.com')
#             search = browser.find_element_by_name('q')
#             search.send_keys(query)
#             search.send_keys(Keys.RETURN)

#             # Wait for the whole google page to load
#             WebDriverWait(browser, 10).until(
#                 EC.visibility_of_element_located((By.ID, "result-stats")))

#             # get all URLs
#             links = browser.find_elements_by_xpath("//*[@id='rso']/*[@class='g']//*[@class='r']//a")
#             urls = [link.get_attribute('href') for link in links]

#             link_counter = 0
#             for url in set(urls):
#                 if link_counter >= 3:
#                     break
#                 if ('google.com' not in url) and ('webcache.googleusercontent.com' not in url):
#                     print(url)
#                     link_counter += 1
#                     # open new blank tab
#                     browser.execute_script("window.open();")
#                     time.sleep(0.05)

#                     # switch to the new window which is second in window_handles array
#                     browser.switch_to_window(browser.window_handles[-1])

#                     browser.get(url)

# sf = Search()
# sf.search_category("search google for civil war")
