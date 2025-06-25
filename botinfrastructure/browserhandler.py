import os
import platform
import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import FakeUserAgent
from .utility import *  
from .config_manager import config_manager
import asyncio
from concurrent.futures import ThreadPoolExecutor


# Configuração de logging
logger = logging.getLogger('BrowserHandler')
logger.setLevel(logging.INFO)

class BrowserHandler:
    def __init__(self, site, profile, proxy, profile_folder):
        self.profile = profile
        self.proxy = proxy
        self.site = site
        self.utility = Utility()
        self.driver = None
        self.ua = FakeUserAgent()
        self.user_agent = self.ua.random
        self.profile_folder = profile_folder

    def close(self):
        self.driver.quit()   
        
    def measure_page_load_time(self, url):
        start_time = time.time()
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        end_time = time.time()
        load_time = end_time - start_time
        logger.info(f"Page loaded in {load_time:.2f} seconds.")
        return load_time
 
        
    # Add a new method to return the initialized driver
    def get_driver(self):
        return self.driver

    async def _random_sleep(self, min_seconds=1, max_seconds=4):
        sleep_time = random.uniform(min_seconds, max_seconds)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds.")
        await asyncio.sleep(sleep_time)

    def _initialize_webdriver_options(self):
        """Initialize Chrome options for WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-file-cookies")
        chrome_options.add_argument(f"user-agent={self.user_agent}")
        chrome_options.add_argument(f"--user-data-dir={self.profile_folder+self.profile}")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--log-path=chromedriver.log")
        chrome_options.add_argument("--remote-debugging-port=9222") 
        return chrome_options

    async def async_initialize_driver(self):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor()
        await loop.run_in_executor(executor, self.initialize_driver)       


    def initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        try:
            chrome_options = self._initialize_webdriver_options()
            os_type = platform.system()
            print("os_type: ", os_type)
            if os_type == "Windows":
                # Define o caminho da pasta root do projeto
                #root_path = os.path.abspath(os.path.dirname(__file__))
                #print("root_path: ", root_path)
                # Define os caminhos relativos a partir da pasta root
                #chrome_binary_path = os.path.join(root_path, "chrome-win64", "chrome.exe")
                #chrome_driver_path = os.path.join(root_path, "chrome-win64", "chromedriver.exe")
                chrome_binary_path = os.path.join(os.getcwd(), "c:\\chrome-win64\\chrome.exe")
                chrome_driver_path = os.path.join(os.getcwd(), "c:\\chrome-win64\\chromedriver.exe")
                self.service = ChromeService(executable_path=chrome_driver_path, enable_verbose_logging = True)
                chrome_options.binary_location = chrome_binary_path   
            elif os_type == "Linux":
                chrome_binary_path = "/usr/bin/google-chrome-stable"
                chrome_driver_path = "./chromedriver"
                chrome_options.add_argument('--headless')
                self.service = ChromeService(ChromeDriverManager().install())
            else:
                raise Exception("Unsupported operating system.")
            
            self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        except Exception as e:
            logger.error(f"Exception occurred while initializing driver: {e}")
            self.utility.print_exception()
            raise

    def validate_bot(self):
        """Validate if the bot is detected by the site."""
        if not self.driver:
            logger.error("Driver not initialized.")
            raise Exception("Driver not initialized.")
        result = {"bot_detected": False, "error": None}
        try:
            self.driver.execute_script("window.open('', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get("https://www.google.com")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(self.site)
            search_box.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
            )
            self.driver.find_element(By.CSS_SELECTOR, "h3").click()
            #self._random_sleep()
            if self.driver.find_elements(By.XPATH, config_manager.get_xpath('cloudflare', 'challenge_stage')):
                logging.warning(f"Bot detected on site: {self.site}")
                result["bot_detected"] = True
                return False
            return True
        except Exception as e:
            logger.error(f"Exception occurred during bot validation: {e}")
            self.utility.print_exception()
            result["error"] = str(e)
            raise    
        
    def load_and_validate_page(self, url):
        """Carrega uma página, valida os dados e mede o tempo de carregamento."""
        start_time = time.time()  # Marca o tempo de início
        self.driver.get(url)  # Carrega a página
        # Implemente sua lógica de validação de dados aqui...
        
        # Verificação de bloqueio pode ser parte de validate_bot ou um novo método
        bot_detected = self.validate_bot()  # Retorna False se bot for detectado
        
        load_time = time.time() - start_time  # Calcula o tempo de carregamento
        logger.info(f"Tempo de carregamento da página: {load_time:.2f} segundos.")
        
        # Log de detecção de bot
        if bot_detected:
            logger.info("Nenhum bloqueio detectado.")
        else:
            logger.warning("Bloqueio de bot detectado!")
        
        # Retorne informações relevantes como parte do resultado
        return {
            "load_time": load_time,
            "bot_detected": not bot_detected,
            # Inclua outras métricas ou informações necessárias
        }  

    def execute(self):
        """Execute the main operation."""
        try:
            self.initialize_driver()
            #result = self.load_and_validate_page(self.site)
            #print(result)
            #if(self.validate_bot()):
            return self.driver
            
        except Exception as e:
            logger.error(f"Exception occurred during execution: {e}")
            self.utility.print_exception()
            raise
