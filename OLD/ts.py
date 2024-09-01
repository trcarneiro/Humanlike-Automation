import logging
import json
from botinfrastructure.browserhandler import BrowserHandler
from botinfrastructure.webpagehandler import WebPageHandler
from db import DynamicDataHandler
import re
from datetime import datetime, date
import asyncio
from datetime import datetime  
from wt_scrapydata import SquadronScraper 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

   
   
logging.info("Starting Squadron Scraper")
try:
    with open('db_config.json', 'r') as f:
        config = json.load(f)
    DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
    browser_handler = BrowserHandler(site="https://warthunder.com", profile="warthunder", proxy=None, profile_folder="profiles")
    web_handler = WebPageHandler(browser_handler.execute())
    scraper = SquadronScraper(web_handler)
    dynamic_data_handler = DynamicDataHandler(DATABASE_URI)
    
    info = asyncio.run(scraper.get_current_tournaments())
    print(info)
    #info = asyncio.run(scraper.get_squadron_leaderboard_info(num_clans=100))
    
    
    logging.info("Data collection and database insertion completed successfully.")
except json.JSONDecodeError as e:
    logging.error("Failed to parse JSON configuration: %s", e, exc_info=True)
except Exception as e:
    logging.exception("An unexpected error occurred during the squadron scraping process: %s", e)
finally:
    browser_handler.close()
    logging.info("Squadron Scraper has finished running.")