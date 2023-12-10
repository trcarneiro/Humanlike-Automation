from browserhandler import BrowserHandler
from webpageanalyzer import WebpageAnalyzer

def test_webpage_analyzer():
    site = "https://warthunder.com/en/community/clansleaderboard/"
    profile = "01"
    proxy = ""
    profile_folder = "profiles/"
    ai_api_key = "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"

    browser_handler = BrowserHandler(site, profile, proxy, profile_folder)
    browser_handler.initialize_driver()

    webpage_analyzer = WebpageAnalyzer(browser_handler.get_driver(), ai_api_key)
    result = webpage_analyzer.analyze_page(site)
    print(result)

    assert 'url' in result
    assert 'elements' in result
    assert 'gpt3_analysis' in result

    browser_handler.close()

if __name__ == "__main__":
    test_webpage_analyzer()
