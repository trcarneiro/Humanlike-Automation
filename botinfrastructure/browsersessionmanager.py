import asyncio
import logging
from selenium.common.exceptions import WebDriverException
from .browserhandler import BrowserHandler
from .webpagehandler import WebPageHandler
import uuid
from uuid import uuid4
import time      
import random

# Configuração para logar em um arquivo
logging.basicConfig(level=logging.INFO, filename='BrowserSessionManager.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
# Configure logging
'''logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='squadron_scraper.log',
                    filemode='w')'''


class BrowserSessionManager:
    def __init__(self, max_instances=10):
        self.max_instances = max_instances
        self.active_sessions = []
        self.failed_attempts = 0
        self.queue = asyncio.Queue()

        # Cria e configura o logger
        #self.logger = logging.getLogger('').addHandler(console_handler)
        # Cria e configura o logger
        self.logger = logging.getLogger('BrowserSessionManager')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(filename='BrowserSessionManager.log', mode='w')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    async def initialize_session(self, site, profile, proxy, profile_folder):
        if len(self.active_sessions) >= self.max_instances:
            logging.error("Maximum number of browser instances reached.")
            return None
        
        session_id = uuid4()
        try:
            browser_handler = BrowserHandler(site=site, profile=profile, proxy=proxy, profile_folder=profile_folder)
            web_handler = WebPageHandler(browser_handler.execute())
            session_info = {'id': session_id, 'handler': web_handler}
            self.active_sessions.append(session_info['id'])
            return session_info
        except Exception as e:
            logging.error(f"Error initiating browser session: {e}")
            # Handle the failure asynchronously if needed
            await self.handle_failure()  # Ensure handle_failure is async or remove await if not
            return None

    async def handle_failure(self):
        self.failed_attempts += 1
        if self.failed_attempts < 3:
            logging.warning("Attempting to restart browser session...")
            await asyncio.sleep(1)  # Add a short delay before retry
        else:
            logging.error("Consecutive failures in starting browser session. Check connection or configurations.")

    async def close_session(self, session_info):
        try:
            session_info['handler'].close()
            self.active_sessions.remove(session_info['id'])
            logging.info("Browser session closed.")
        except Exception as e:
            logging.error(f"Error closing browser session: {e}")

    async def restart_session(self, web_handler):
        for index, (browser_handler, _web_handler, session_params) in enumerate(self.active_sessions):
            if _web_handler == web_handler:
                await self.close_session(web_handler)
                # Reinitialize session with the same parameters
                return await self.initialize_session(**session_params)
        logging.error("Session not found for restart.")

    async def add_urls_to_queue(self, urls):
        for url in urls:
            await self.queue.put(url)

    async def process_url(self, url, scraper_function):
        session_id = str(uuid4())
        start_time = time.perf_counter()
        self.logger.info(f"[{session_id}] Starting URL processing: {url}")
        
        session_info = await self.initialize_session(site="https://warthunder.com", profile="warthunder", proxy=None, profile_folder="profiles")
        
        # Verifica se session_info é None antes de prosseguir
        if session_info is None:
            self.logger.error(f"[{session_id}] Failed to initialize session for URL: {url}. Skipping.")
            return  # Sai da função se não conseguir iniciar a sessão

        web_handler = session_info['handler']
        if web_handler:
            try:
                await scraper_function(web_handler, url)
                end_time = time.perf_counter()
                duration = end_time - start_time
                self.logger.info(f"[{session_id}] Finished processing URL: {url} in {duration:.2f} seconds")
            except Exception as e:
                self.logger.error(f"[{session_id}] Error processing URL {url}: {e}")
            finally:
                # Supondo que web_handler.close() seja síncrono; se for assíncrono, deve ser ajustado
                web_handler.close()
        else:
            self.logger.error(f"[{session_id}] Failed to initialize session for URL: {url}")


    async def run_scraping_tasks(self, urls, scraper_function):
        await self.add_urls_to_queue(urls)
    
        async def process_queue():
            while not self.queue.empty():
                url = await self.queue.get()
                self.logger.info(f"Queue size before processing: {self.queue.qsize()}")

                start_time = time.time()
                task_id = hash(url) % 100  # Exemplo simples para gerar um ID curto
                self.logger.info(f"[Task {task_id}] Starting URL processing: {url}")
                print(f"[Task {task_id}] Starting URL processing: {url}")
                await self.process_url(url, scraper_function)

                #s = random.randint(1, 15)
                #print("Processing URL: ", url)
                #print(f"Sleeping for {s} seconds")
                await asyncio.sleep(random.randint(1, 5)) 
                self.logger.info(f"Queue size after processing: {self.queue.qsize()}")
                self.queue.task_done()
                end_time = time.time()
                print(f"[Task {task_id}] Finished URL processing: {url} in {end_time - start_time:.2f} seconds")
                self.logger.warning(f"[Task {task_id}] Finished URL processing: {url} in {end_time - start_time:.2f} seconds")
        
        tasks = [asyncio.create_task(process_queue()) for _ in range(min(self.max_instances, len(urls)))]
        await asyncio.gather(*tasks)


'''if __name__ == "__main__":
    urls = ['https://www.google.com', 'https://www.wikipedia.org', 'https://www.python.org', 'https://www.github.com', 'https://www.stackoverflow.com']
    manager = BrowserSessionManager(max_instances=3)
    asyncio.run(manager.run_scraping_tasks(urls, lambda x, y: print(x, y)))
    print("All tasks completed.")
    logging.info("All tasks completed.")'''