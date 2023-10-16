import random
import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from utils import Utility
from webdriver import BrowserHandler

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Timeouts and sleep settings
MIN_SLEEP = 2
MAX_SLEEP = 5
DEFAULT_TIMEOUT = 10

class WebPageHandler:
    """
    A class to handle interactions with a web page using Selenium WebDriver.
    """

    def __init__(self, site, user, proxy):
        """
        Initialize the WebPageHandler with a site, user, and proxy.
        """
        self.webdriver = BrowserHandler(site, user, proxy)
        self.driver = self.webdriver.execute()
        self.utils = Utility()

    def _wait_for_element(self, xpath, timeout=DEFAULT_TIMEOUT, clickable=False):
        """
        Waits for an element to appear on the web page.
        """
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        try:
            return WebDriverWait(self.driver, timeout).until(condition((By.XPATH, xpath)))
        except (TimeoutException, WebDriverException) as e:
            logger.error(f"An error occurred while waiting for element: {e}")
            self.utils.print_exception()
            return None

    def _random_sleep(self):
        """
        Pauses the execution for a random amount of time.
        """
        sleep_duration = random.uniform(MIN_SLEEP, MAX_SLEEP)
        logger.info(f"Sleeping for {sleep_duration:.2f} seconds.")
        time.sleep(sleep_duration)
        
    # ... (other methods remain unchanged for brevity)

    def get_elements_by_xpath(self, xpath):
        """
        Gets multiple elements by their XPath.
        """
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            return elements
        except WebDriverException as e:
            logger.error(f"An error occurred while trying to find the elements: {e}")
            return None

    def get_element_by_xpath(self, xpath):
        """
        Gets a single element by its XPath.
        """
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element
        except WebDriverException as e:
            logger.error(f"An error occurred while trying to find the element: {e}")
            return None

    def open_link(self, link):
        """
        Opens a new link in the web driver.
        """
        try:
            self.driver.get(link)
        except WebDriverException as e:
            logger.error(f"An error occurred while trying to open the link: {e}")
            return None
