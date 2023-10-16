import os
import platform
import random
import time
import logging
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utils import Utility  # Certifique-se de importar a classe Utility corretamente

# Configuração de logging
logger = logging.getLogger('BrowserHandler')
logger.setLevel(logging.INFO)

class BrowserHandler:
    def __init__(self, site, profile, proxy):
        self.profile = profile
        self.proxy = proxy
        self.site = site
        self.utility = Utility()
        self.driver = None

    def _random_sleep(self, min_seconds=5, max_seconds=10):
        """Pause the execution for a random time."""
        sleep_time = random.uniform(min_seconds, max_seconds)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds.")
        time.sleep(sleep_time)

    def _initialize_webdriver_options(self):
        """Initialize Chrome options for WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-file-cookies")
        chrome_options.add_argument(f"--user-data-dir={os.path.join(os.getcwd(), 'profiles', self.profile)}")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--log-path=chromedriver.log")
        return chrome_options

    def initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        try:
            chrome_options = self._initialize_webdriver_options()
            os_type = platform.system()
            if os_type == "Windows":
                self.driver = webdriver.Chrome(executable_path="c:\\chrome-win64\\chromedriver.exe", options=chrome_options)
            elif os_type == "Linux":
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            else:
                raise Exception("Unsupported operating system.")
        except Exception as e:
            logger.error(f"Exception occurred while initializing driver: {e}")
            self.utility.print_exception()
            raise

    def validate_bot(self):
        """Validate if the bot is detected by the site."""
        if not self.driver:
            logger.error("Driver not initialized.")
            raise Exception("Driver not initialized.")
        try:
            self.driver.get(self.site)
            self.driver.find_element(By.NAME, "q").send_keys("test")
        except Exception as e:
            logger.error(f"Exception occurred during bot validation: {e}")
            self.utility.print_exception()
            raise

    def execute(self):
        """Execute the main operation."""
        try:
            self.initialize_driver()
            self.validate_bot()
        except Exception as e:
            logger.error(f"Exception occurred during execution: {e}")
            self.utility.print_exception()
            raise
