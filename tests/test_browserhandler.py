# test_browserhandler.py
import pytest
from botinfrastructure.browserhandler import BrowserHandler

@pytest.fixture
def setup_browserhandler():
    # Substitua com os parâmetros apropriados
    site = "https://warthunder.com/en/community/clansleaderboard/page/1/?type=hist"
    profile = "profile_name"
    proxy = None  # ou configure seu proxy
    profile_folder = "/path/to/profile_folder"
    browser_handler = BrowserHandler(site, profile, proxy, profile_folder)
    yield browser_handler
    browser_handler.close()

def test_load_and_validate_page(setup_browserhandler):
    browser_handler = setup_browserhandler
    browser_handler.initialize_driver()
    result = browser_handler.load_and_validate_page(browser_handler.site)
    #print(result)
    assert result["load_time"] < 20, "Tempo de carregamento é muito alto"
    assert not result["bot_detected"], "Bot foi detectado"
