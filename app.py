from fastapi import FastAPI
from selenium import webdriver
from wt_scrapydata import SquadronScraper

app = FastAPI()

@app.get("/squadrons/")
async def get_squadron_info():
    driver = webdriver.Chrome()  # Ou qualquer outro driver que você preferir
    scraper = SquadronScraper(driver)
    info = scraper.get_squadron_leaderboard_info()
    driver.quit()  # Não se esqueça de fechar o navegador
    return {"squadrons": info}
