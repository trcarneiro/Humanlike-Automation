import logging
import time
from screen_logic import LinkedInScreenLogic
from botinfrastructure import *
import asyncio

class LinkedInJobScraperBot:
    def __init__(self): 
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of log messages

        # Console handler for debug output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Capture all levels on console
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info("Initializing LinkedInJobScraperBot")

        self.site = 'https://www.linkedin.com'
        self.user = 'trcarneiro@outlook.com'
        self.password = 'C3po007*a1'
        self.proxy = None
        self.profile_folder = './profiles'
        self.webdriver = BrowserHandler(self.site, self.user, self.proxy, self.profile_folder)
        self.driver = self.webdriver.execute()
        self.web_handler = WebPageHandler(self.driver)
        self.screen_logic = LinkedInScreenLogic(self.web_handler)
        self.search_term = 'python developer'
        self.resume = r'C:\Users\Thiago\Desktop\Resume.pdf'

    async def run(self):
        self.logger.info("Starting LinkedInJobScraperBot")
        self.screen_logic.login(self.user, self.password)
        all_jobs = self.screen_logic.search_jobs(self.search_term)
 
        if all_jobs:
            for job in all_jobs:
                print(job)
                #await self.screen_logic.easy_apply(job['link'], self.resume)

        #SECTION - time.sleep(6000)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = LinkedInJobScraperBot()
    asyncio.run(bot.run()) 