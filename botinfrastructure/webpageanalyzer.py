import logging
from selenium import webdriver
from bs4 import BeautifulSoup, Tag
import json
from .utility import Utility
from .ai_handler import AiAnalyzer
from .webpagehandler import WebPageHandler # Importe ou defina esta classe


class WebpageAnalyzer:
    def __init__(self, driver, ai_api_key):
        self.driver = driver
        self.ai_analyzer = AiAnalyzer()  
        self.webpagehandler = WebPageHandler(self.driver)# Inicializa o analisador de IA

    def load_page(self, url):
        self.driver.get(url)    

    def download_html_content(self):
        return self.driver.page_source

    def parse_html_for_elements(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(['a', 'button', 'input', 'select', 'div'])
        return elements

    def generate_xpaths(self, elements):
        xpaths = []
        for element in elements:
            if isinstance(element, Tag):
                xpaths.append(self.webpagehandler.get_xpath(element))
        return xpaths

    def analyze_page(self, url):
        self.load_page(url)
        html_content = self.download_html_content()
        elements = self.parse_html_for_elements(html_content)
        xpaths = self.generate_xpaths(elements)

        data = {"url": url, "elements": []}
        for element, xpath in zip(elements, xpaths):
            element_data = {
                "tag": element.name,
                "text": element.get_text(strip=True),
                "xpath": xpath,
                "attributes": {attr: element[attr] for attr in element.attrs}
            }
            data["elements"].append(element_data)

        # Adicionando análise com GPT-3
        gpt3_response = self.ai_analyzer.analyze_elements(data["elements"])
        data["gpt3_analysis"] = gpt3_response

        return json.dumps(data, indent=4)
