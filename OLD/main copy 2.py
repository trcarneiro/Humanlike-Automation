import logging
import asyncio
from screen_logic import LinkedInScreenLogic
from botinfrastructure import BrowserHandler, WebPageHandler
from data_handler import DataHandler
from config import Config

class LinkedInJobScraperBot:
    def __init__(self):
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of log messages

        # Console handler for debug output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for saving logs to a file
        file_handler = logging.FileHandler('linkedin_scraper.log')
        file_handler.setLevel(logging.ERROR)  # Log only errors and critical issues to the file
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        self.resume = r'C:\Users\Thiago\Desktop\Resume.pdf'

        self.logger.info("Initializing LinkedInJobScraperBot")

        self.data_handler = DataHandler()
        self.profile_folder = Config.PROFILES_FOLDERS

    def setup_user_driver(self, usernetworksdata, networkdata, proxy=''):
        """Setup the WebDriver with the user's LinkedIn credentials."""
        try:
            self.webdriver = BrowserHandler(networkdata.loginurl, usernetworksdata.loginname, proxy, self.profile_folder)
            self.driver = self.webdriver.execute()
            self.web_handler = WebPageHandler(self.driver)
            self.screen_logic = LinkedInScreenLogic(self.web_handler)
            self.logger.info(f"WebDriver setup completed for user: {usernetworksdata.loginname}")
        except Exception as e:
            self.logger.error(f"Failed to set up WebDriver: {e}", exc_info=True)

    async def run(self):
        try:
            self.logger.info("Starting LinkedInJobScraperBot")

            # Step 1: Get system user
            user = self.data_handler.get_system_user("miapson007x@gmail.com")
            if not user:
                self.logger.error("System user not found.")
                return

            self.logger.info(f"System user found: {user.username}")
            # Step 2: Check registered networks
            usernetworksdata = self.data_handler.get_user_network(user.id, 'linkedin')
            if not usernetworksdata:
                self.logger.error("User network data for LinkedIn not found.")
                return

            self.logger.info(f"User network data found: {usernetworksdata}")
            # Step 3: Get network data
            networkdata = self.data_handler.get_network_data(usernetworksdata.networkid)
            if not networkdata:
                self.logger.error("Network data not found.")
                return

            self.logger.info(f"Network data found: {networkdata}")
            # Step 5: Get user keywords to search
            userkeywords = self.data_handler.get_keywords_by_criteria(id=1)
            if not userkeywords:
                self.logger.warning("No keywords found.")
                return
            
            userkeywords = userkeywords[0]
            
            print(userkeywords.keyword)

            self.logger.info(f"Keywords found: {userkeywords.keyword}")
            
            # Step 8: Get user data to apply for jobs
            resumes = self.data_handler.get_resumes_by_criteria(user_id=user.id)
            if not resumes:
                self.logger.error("No resumes found for the user.")
                return
        
            resume = resumes[0]  # Assuming we're using the first resume
            
            # Step 6: Get filters for the keyword
            filters = self.data_handler.get_filters_by_criteria(id=2)
            if not filters:
                self.logger.warning("No filters found.")
                return
            
            self.logger.info(f"Filters found: {filters}")
            
            self.setup_user_driver(usernetworksdata, networkdata)

            # Step 4: Login to LinkedIn
            login_success = self.screen_logic.login(usernetworksdata.loginname, usernetworksdata.loginpassword)
            if not login_success:
                self.logger.error("Failed to log in to LinkedIn.") 
                return False
    

            # Step 7: Search for jobs
            self.screen_logic.is_logged_in(usernetworksdata.loginname, usernetworksdata.loginpassword)
            all_jobs = self.screen_logic.search_jobs(userkeywords.keyword, filters)
            if not all_jobs:
                self.logger.info(f"No jobs found for keyword: {userkeywords.keyword}")
                return

            # Step 9: Apply for jobs
            for job in all_jobs:
                #(job['link'])
                self.logger.info(f"Applying for job: {job['title']}")
                #await self.screen_logic.easy_apply(job['link'], user, resume.file_path)

            self.logger.info("LinkedInJobScraperBot finished running.")

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = LinkedInJobScraperBot()
    asyncio.run(bot.run())
