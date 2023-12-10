import json
import charset_normalizer 
import logging
from bs4 import BeautifulSoup
import re
import openai

class AiAnalyzer:
    def __init__(self, api_key_file='apikeys.txt', html_file='page.html', model='gpt-3.5-turbo'):
        self.api_key_file = api_key_file
        self.html_file = html_file
        self.model = model
        self.api_keys = self.read_api_keys()
        self.html_content = self.read_html_file()

    def read_api_keys(self):
        try:
            with open(self.api_key_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except Exception as e:
            logging.error(f"Error reading API keys: {e}")
            return []

    def read_html_file(self):
        try:
            with open(self.html_file, 'rb') as file:
                result = charset_normalizer.detect(file.read())
                file.seek(0)
                return file.read().decode(result['encoding'])
        except FileNotFoundError:
            logging.error("HTML file not found.")
            return None

    def query_gpt(self, prompt):
        try:
            openai.api_key = self.api_keys[0]  # Assuming the first key is the one we want to use
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"Error querying GPT: {e}")
            return None

    def identify_item_containers(self):
        try:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            return soup.find_all(['div', 'section', 'article'], {'class': re.compile(r'item|product|listing', re.I)})
        except Exception as e:
            logging.error(f"Error identifying item containers: {e}")
            return []

    def analyze_html(self):
        if not self.html_content:
            return None
        
        item_containers = self.identify_item_containers()
        analyzed_data = []
        prompt = "Analyze this HTML content for interactive elements:\n" + self.html_content

        assistant_message = self.query_gpt(prompt)
        if assistant_message:
            analyzed_data.append({"assistant_message": assistant_message})
        
        return analyzed_data

    def analyze_html_in_chunks(self, chunk_size=5000):
        if len(self.html_content) > chunk_size:
            chunks = [self.html_content[i:i+chunk_size] for i in range(0, len(self.html_content), chunk_size)]
            return [self.analyze_html_chunk(chunk) for chunk in chunks]
        else:
            return [self.analyze_html()]

    def analyze_html_chunk(self, chunk):
        prompt = "Analyze this HTML chunk for interactive elements:\n" + chunk
        return self.query_gpt(prompt)

    def run_analysis(self):
        if not self.api_keys:
            logging.error("No API keys found.")
            return None
        return self.analyze_html_in_chunks()
    
    def analyze_specific_html_section(self, html_section):
        """
        Analisa uma seção específica do HTML.

        :param html_section: String contendo a seção HTML a ser analisada.
        :return: Dados analisados.
        """
        try:
            item_containers = self.identify_item_containers(html_section)
            analyzed_images = self.analyze_images(item_containers)
            analyzed_fields = self.analyze_item_fields(item_containers)

            prompt = f"Analyze these already identified fields and images:\n{json.dumps(analyzed_fields)}\n{json.dumps(analyzed_images)}"
            assistant_message = self.query_gpt(prompt)

            if assistant_message:
                return {
                    "assistant_message": assistant_message,
                    "analyzed_fields": analyzed_fields,
                    "analyzed_images": analyzed_images
                }
        except Exception as e:
            logging.error(f"An error occurred while analyzing specific HTML section: {e}")
            return None
        
    def analyze_elements(self, elements):
        """
        Analisa os elementos HTML extraídos, utilizando a API GPT.

        :param elements: Lista de elementos HTML a serem analisados.
        :return: Resposta do GPT com análise dos elementos.
        """
        # Construir prompt para GPT
        prompt = "Please analyze the following HTML elements and provide insights on their functionality:\n"
        for element in elements:
            prompt += f"Tag: {element['tag']}, Text: {element['text']}, XPath: {element['xpath']}\n"

        # Fazer consulta ao GPT
        gpt_response = self.query_gpt(prompt)

        return gpt_response