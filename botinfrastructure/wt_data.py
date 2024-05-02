from datetime import datetime, date

from webpagehandler import WebPageHandler

class SquadronScraper:
    def __init__(self):
        self.web_handler = WebPageHandler()
        self.clan_urls = {
            "WTBRA": ('War Thunder Brasil', 'https://warthunder.com/en/community/claninfo/War%20Thunder%20Brasil'),
            "WTBRZ": ('War Thunder Brazil', 'https://warthunder.com/en/community/claninfo/War%20Thunder%20Brazil'),
            "WTBRX": ('WarThunder Brasil', 'https://warthunder.com/en/community/claninfo/WarThunder%20Brasil'),
            "WTBRY": ('War Thunder BrasiI', 'https://warthunder.com/pt/community/claninfo/War%20Thunder%20BrasiI'),
            "WTBRP": ('War Thunder Brasil Pontuacao', 'https://warthunder.com/pt/community/claninfo/War%20Thunder%20Brasil%20%20Pontuacao')
        } 

    @staticmethod
    def cf_decode_email(self, encoded_string: str) -> str:
        r = int(encoded_string[:2], 16)
        email = ''.join([chr(int(encoded_string[i:i + 2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
        return email

    '''def get_squadron_leaderboard_info(self) -> list[dict]:
        
        # If forcing a new request or the file doesn't exist, make a new request
         # If forcing a new request or the file doesn't exist, make a new request
         
         
        response = requests.get("https://warthunder.com/pt/community/clansleaderboard/?type=hist")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #print(soup)

        # Encontrar a tabela de classificação dos esquadrões
        leaderboard_table = soup.find('table', class_='leaderboards__table-wrapper')

        # Encontrar todas as linhas da tabela, excluindo o cabeçalho
        rows = leaderboard_table.find_all('tr')[1:] 

        squadrons_info = []

        for row in rows:
            columns = row.find_all('td')
            if columns:
                squadron_info = {
                    'place': columns[0].text.strip(),
                    'name': columns[1].find('a').text.strip(),
                    'duel_ratio': columns[2].text.strip(),
                    'members': columns[3].text.strip(),
                    'air_targets_destroyed': columns[4].text.strip(),
                    'ground_targets_destroyed': columns[5].text.strip(),
                    'deaths': columns[6].text.strip(),
                    'flight_time': columns[7].text.strip()
                }
            print(squadron_info)
                #squadrons_info.append(squadron_info)

        return squadrons_info'''
    
    def get_squadron_leaderboard_info(self):
        url = "https://warthunder.com/pt/community/clansleaderboard/?type=hist"
        self.web_handler.open_link(url)

        # Supondo que a tabela de classificação tenha um ID ou classe única para facilitar a localização
        leaderboard_xpath = "//table[@class='leaderboards__table-wrapper']"
        self.web_handler._wait_for_element(leaderboard_xpath)  # Espera pela tabela

        # Supondo que exista uma maneira de iterar sobre os elementos da tabela com o Selenium
        rows = self.web_handler.get_elements_by_xpath(f"{leaderboard_xpath}//tr[position()>1]")
        squadrons_info = []

        for row in rows:
            squadron_info = {
                'place': self.web_handler.get_text_on_element(row, ".//td[1]").strip(),
                'name': self.web_handler.get_text_on_element(row, ".//td[2]/a").strip(),
                'duel_ratio': self.web_handler.get_text_on_element(row, ".//td[3]").strip(),
                'members': self.web_handler.get_text_on_element(row, ".//td[4]").strip(),
                'air_targets_destroyed': self.web_handler.get_text_on_element(row, ".//td[5]").strip(),
                'ground_targets_destroyed': self.web_handler.get_text_on_element(row, ".//td[6]").strip(),
                'deaths': self.web_handler.get_text_on_element(row, ".//td[7]").strip(),
                'flight_time': self.web_handler.get_text_on_element(row, ".//td[8]").strip()
            }
            squadrons_info.append(squadron_info)

        return squadrons_info
    
if __name__ == "__main__":
    scraper = SquadronScraper()
    info = scraper.get_squadron_leaderboard_info()
    print(info)
    #discordbot.send_squadron_info(info)