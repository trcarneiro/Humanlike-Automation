import asyncio
import logging
from selenium.common.exceptions import WebDriverException
from .browserhandler import BrowserHandler
from .webpagehandler import WebPageHandler
import uuid

logging.basicConfig(level=logging.INFO)

class BrowserSessionManager:
    def __init__(self, max_instances=5):
        self.max_instances = max_instances
        self.active_sessions = []
        self.failed_attempts = 0
        self.queue = asyncio.Queue()
        self.logger = logging.getLogger('BrowserSessionManager')

    async def initialize_session(self, site, profile, proxy, profile_folder):
        if len(self.active_sessions) >= self.max_instances:
            logging.error("Máximo de instâncias de navegador atingido.")
            return None
        session_id = uuid.uuid4()  # Gera um identificador único
        self.logger.info(f"Iniciando nova sessão de navegador com ID {session_id}")

        session_params = {'site': site, 'profile': profile, 'proxy': proxy, 'profile_folder': profile_folder}
        try:
            # Directly instantiate the browser handler and web page handler without awaiting
            browser_handler = BrowserHandler(site=site, profile=profile, proxy=proxy, profile_folder=profile_folder)
            web_handler = WebPageHandler(browser_handler.execute())  # This is synchronous
            self.active_sessions.append((browser_handler, web_handler, session_params))
            return web_handler
        except Exception as e:
            logging.error(f"Erro ao iniciar sessão do navegador: {e}")
            await self.handle_failure()  # Ensure handle_failure is async or remove await if not
            return None


    async def handle_failure(self):
        self.failed_attempts += 1
        if self.failed_attempts < 3:
            logging.warning("Attempting to restart browser session...")
            await asyncio.sleep(1)  # Add a short delay before retry
        else:
            logging.error("Consecutive failures in starting browser session. Check connection or configurations.")

    async def close_session(self, web_handler):
        for index, (browser_handler, _web_handler, _) in enumerate(self.active_sessions):
            if _web_handler == web_handler:
                await browser_handler.close()
                self.active_sessions.pop(index)
                logging.info("Browser session closed.")
                return

    async def restart_session(self, web_handler):
        for index, (browser_handler, _web_handler, session_params) in enumerate(self.active_sessions):
            if _web_handler == web_handler:
                await self.close_session(web_handler)
                # Reinitialize session with the same parameters
                return await self.initialize_session(**session_params)
        logging.error("Session not found for restart.")

    '''async def process_urls(self, scraper_function):
        while not self.queue.empty():
            url = await self.queue.get()
            web_handler = await self.initialize_session(**(self.active_sessions[0][2]))  # Assuming parameters of the first session are reusable
            if web_handler:
                try:
                    await scraper_function(web_handler, url)
                    logging.info(f"Completed scraping for {url}")
                except Exception as e:
                    logging.error(f"Error scraping {url}: {e}")
                    await self.restart_session(web_handler)
                finally:
                    await self.close_session(web_handler)
            else:
                logging.error(f"Failed to initialize web handler for URL: {url}")
            self.queue.task_done()'''
    async def process_urls(self, scraper_function):
        while not self.queue.empty():
            url = await self.queue.get()
            session_info = self.active_sessions[0][2]  # Assuming parameters of the first session are reusable
            loop = asyncio.get_running_loop()

            # Create a web handler asynchronously
            web_handler, session_id = await loop.run_in_executor(None, lambda: self.initialize_session(**session_info))

            if web_handler:
                try:
                    await loop.run_in_executor(None, lambda: scraper_function(web_handler, url))
                    self.logger.info(f"Completed scraping for {url}")
                except Exception as e:
                    self.logger.error(f"Error scraping {url}: {e}")
                    await self.restart_session(web_handler)
                finally:
                    await loop.run_in_executor(None, web_handler.close)
            else:
                self.logger.error(f"Failed to initialize web handler for URL: {url}")
            self.queue.task_done()
        

    async def add_urls_to_queue(self, urls):
        for url in urls:
            await self.queue.put(url)

    async def run_scraping_tasks(self, urls, scraper_function):
        await self.add_urls_to_queue(urls)
        tasks = [self.process_urls(scraper_function) for _ in range(self.max_instances)]
        await asyncio.gather(*tasks)
        
