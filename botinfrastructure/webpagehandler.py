import random
import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from .utility import *  
from .browserhandler import *  

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebPageHandler:

    def __init__(self, driver):
        self.driver = driver
        self.utils = Utility()

    def _wait_for_element(self, xpath, timeout=10, clickable=False):
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        try:
            return WebDriverWait(self.driver, timeout).until(condition((By.XPATH, xpath)))
        except (TimeoutException, WebDriverException) as e:
            logger.error(f"An error occurred while waiting for element: {e} xpath: {xpath}")
            return None
            #raise e  # Relançar a exceção para que o chamador saiba que algo falhou

    def element_exists(self, xpath, timeout=10):
        """
        Checks if an element exists on the page within a given timeout.
        """
        condition = EC.presence_of_element_located
        try:
            WebDriverWait(self.driver, timeout).until(condition((By.XPATH, xpath)))
            return True
        except (TimeoutException, WebDriverException):
            logger.error(f"An error occurred while trying to element exists : {xpath}")
            return False

    def click_element(self, xpath):
        """
        Clicks an element if it exists; logs an error otherwise.
        """
        try:
            if self.element_exists(xpath):
                element = self._wait_for_element(xpath, clickable=True)
                element.click()
                self._random_sleep()
                return True
            else:
                logger.error(f"Element not found: {xpath}")
                return False
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while trying to element exists : {e}{xpath}")

    def click_element_on_element_xpath(self, elem, xpath):
        try:
            element_item =  elem.find_element(By.XPATH, xpath)
            if element_item:
                element_item.click()
                self._random_sleep()
                return True
            else:
                logger.error(f"Element not found: {xpath}")
                return False
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while trying to element exists : {e}{xpath}")
            return None            


    def _random_sleep(self, min_seconds=2, max_seconds=5):
        sleep_duration = random.uniform(min_seconds, max_seconds)
        logger.info(f"Sleeping for {sleep_duration:.2f} seconds.")
        time.sleep(sleep_duration)

    def go_to_element(self, xpath):
        element = self._wait_for_element(xpath, clickable=True)
        if element:
            ActionChains(self.driver).move_to_element(element).click().perform()
            self._random_sleep()

    def send_text(self, xpath, text):
        element = self._wait_for_element(xpath, clickable=True)
        if element:
            element.clear()
            self._random_sleep()
            element.send_keys(text)

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._random_sleep()

    def get_text_by_xpath(self, xpath):
        try:
            if self.element_exists(xpath, timeout= 2):
                element = self._wait_for_element(xpath, clickable=True)
                return element.text
            else:
                logger.error(f"Element not found: {xpath}")
                return False
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while trying to element exists : {e}{xpath}")
            return None
        
    def get_text_on_element(self, elem, xpath):
        try:
            element_item =  elem.find_element(By.XPATH, xpath)
            if element_item:
                return element_item.text
            else:
                logger.error(f"Element not found: {xpath}")
                return False
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while trying to element exists : {e}{xpath}")
            return None    

    def get_link_by_xpath(self, xpath):
        try:
            link = self._wait_for_element(xpath, clickable=True)
            link.click()
            self._random_sleep()
            link = self.utils.paste_from_clipboard()
            if link:
                logger.info(f"Link found: {link}")
                return link
            else:
                logger.warning("Link element found, but it's empty.")
                return None
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"An error occurred while trying to find the link: {e}")
            return None

    def get_elements_by_xpath(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            return elements
        except WebDriverException as e:
            logger.error(f"An error occurred while trying to find the elements: {e}")
            return None

    def get_element_by_xpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element
        except WebDriverException as e:
            logger.error(f"An error occurred while trying to find the element: {e}")
            return None

    def open_link(self, link):
        try:
            self.driver.get(link)
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
            WebDriverWait(self.driver, 10).until(element_present)
            return True
        except WebDriverException as e:
            logging.error(f"An error occurred while trying to open the link: {e}")
            return None
