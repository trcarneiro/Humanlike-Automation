import logging
import json
from botinfrastructure.browserhandler import BrowserHandler
from botinfrastructure.webpagehandler import WebPageHandler
from db import DynamicDataHandler
import re
from datetime import datetime, date
import asyncio
from datetime import datetime



# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='squadron_scraper.log',
                    filemode='w')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger('').addHandler(console_handler)

class SquadronScraper:
    def __init__(self,web_handler):
        self.web_handler = web_handler
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing SquadronScraper")


        self.clan_urls = {
            "WTBRA": ('War Thunder Brasil', 'https://warthunder.com/en/community/claninfo/War%20Thunder%20Brasil'),
            "WTBRZ": ('War Thunder Brazil', 'https://warthunder.com/en/community/claninfo/War%20Thunder%20Brazil'),
            "WTBRX": ('WarThunder Brasil', 'https://warthunder.com/en/community/claninfo/WarThunder%20Brasil'),
            "WTBRY": ('War Thunder BrasiI', 'https://warthunder.com/pt/community/claninfo/War%20Thunder%20BrasiI'),
            "WTBRP": ('War Thunder Brasil Pontuacao', 'https://warthunder.com/pt/community/claninfo/War%20Thunder%20Brasil%20Pontuacao')
        } 

    def convert_date_format(self, date_str):
        try:
            date_str = datetime.strptime(date_str, "%d.%m.%Y")
            date_str = date_str.isoformat()
            #date_str = date_str.date()
            
            return date_str
        except ValueError as e:
            logging.error(f"Data inválida '{date_str}' não pôde ser convertida: {e}")
            return None

    @staticmethod
    def cf_decode_email(encoded_string: str) -> str:
        r = int(encoded_string[:2], 16)
        email = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
        return email
    
    async def get_squadron_leaderboard_info(self, num_clans: int = 1) -> list[dict]:
        self.logger.info("Fetching squadron leaderboard information across multiple pages.")
        base_url = "https://warthunder.com/pt/community/clansleaderboard/page/{}/?type=hist"
        
        squadrons_info = []  # Inicializa fora do loop para acumular dados de todas as páginas
        for page_number in range(1, 30):  # Iterar da página 1 até a página 20
            try:
                url = base_url.format(page_number)
                self.web_handler.open_link(url)
                self.logger.info(f"Opened URL: {url}")
                #print(f"Opened URL: {url}")
                
                leaderboard_xpath = '//*[@id="clan_leaderboard"]/table'
                self.web_handler._wait_for_element(leaderboard_xpath)
                self.logger.info("Found the leaderboard table on page {}".format(page_number))
                
                rows = self.web_handler.get_elements_by_xpath(f"{leaderboard_xpath}//tr[position()>1]")
                for row in rows:
                    link_xpath = ".//td[2]/a"  # Xpath relativo à linha para encontrar o link
                    squadron_info = {
                        'link': self.web_handler.get_attribute_of_element(row, link_xpath, "href"),
                        'place': self.web_handler.get_text_on_element(row, ".//td[1]").strip(),
                        'name': self.web_handler.get_text_on_element(row, link_xpath).strip(),
                        'duel_ratio': self.web_handler.get_text_on_element(row, ".//td[3]").strip(),
                        'members': self.web_handler.get_text_on_element(row, ".//td[4]").strip(),
                        'air_targets_destroyed': self.web_handler.get_text_on_element(row, ".//td[5]").strip(),
                        'ground_targets_destroyed': self.web_handler.get_text_on_element(row, ".//td[6]").strip(),
                        'deaths': self.web_handler.get_text_on_element(row, ".//td[7]").strip(),
                        'flight_time': self.web_handler.get_text_on_element(row, ".//td[8]").strip()
                    }
                    #print(squadron_info)
                    squadrons_info.append(squadron_info)
                    self.logger.debug("Added squadron info: %s", squadron_info['name'])
                    
                    if len(squadrons_info) >= num_clans:
                        self.logger.info(f"Reached the limit of {num_clans} squadrons.")
                        return squadrons_info
                    
            except Exception as e:
                self.logger.error(f"Failed to fetch squadron leaderboard information on page {page_number}: {e}", exc_info=True)
                # Opcional: decidir se continua para a próxima página ou não, dependendo da sua lógica de erro
        
        self.logger.info("Successfully fetched squadron leaderboard information across multiple pages.")
        return squadrons_info

    async def get_squadron_info(self, url: str) -> dict:
        
        self.web_handler.open_link(url)
        self.logger.info(f"Fetching data for URL: {url}")
        
        print(f"Fetching data for URL: {url}")
        
        squadron_info = []  # Inicializa um dicionário para armazenar informações do esquadrão

        # Nome do esquadrão
        squadron_name_xpath = "//div[@class='squadrons-info__title']"
        squadron_name = self.web_handler.get_text_by_xpath(squadron_name_xpath)

        # Número de jogadores
        num_players_xpath = "//div[@class='squadrons-info__meta-item'][contains(text(),'Número de jogadores:')]"
        num_players = self.web_handler.get_text_by_xpath(num_players_xpath).split(": ")[1]
        num_players_text = self.web_handler.get_text_by_xpath(num_players_xpath)

        # Data de criação
        creation_date_xpath = "//div[@class='squadrons-info__meta-item squadrons-info__meta-item--date']"
        creation_date = self.web_handler.get_text_by_xpath(creation_date_xpath).split(": ")[1]
        
        if num_players_text is None:
            self.logger.error(f"Could not find the number of players for URL: {url}")
            num_players = "Unknown"  # or set to a default value or handle the error as needed
        else:
            num_players = num_players_text.split(": ")[1]
            
        '''
        # Estatísticas do esquadrão
        air_targets_destroyed_xpath = "//ul[@class='squadrons-stat__item'][2]/li[2]"
        ground_targets_destroyed_xpath = "//ul[@class='squadrons-stat__item'][2]/li[3]"
        deaths_xpath = "//ul[@class='squadrons-stat__item'][2]/li[4]"
        flight_time_xpath = "//ul[@class='squadrons-stat__item'][2]/li[5]"

        air_targets_destroyed = self.web_handler.get_text_by_xpath(air_targets_destroyed_xpath)
        ground_targets_destroyed = self.web_handler.get_text_by_xpath(ground_targets_destroyed_xpath)
        deaths = self.web_handler.get_text_by_xpath(deaths_xpath)
        flight_time = self.web_handler.get_text_by_xpath(flight_time_xpath).split(" ")[0]  '''

        # Classificação e Atividade do Esquadrão
        squadron_rating_xpath = "//div[@class='squadrons-counter__value'][1]"
        squadron_activity_xpath = "//div[@class='squadrons-counter__value'][2]"

        #squadron_rating = self.web_handler.get_text_by_xpath(squadron_rating_xpath)
        #squadron_activity = self.web_handler.get_text_by_xpath(squadron_activity_xpath)
        # Quando você coletar a creation_date, converta-a antes de adicionar ao dicionário
        creation_date_raw = self.web_handler.get_text_by_xpath(creation_date_xpath).split(": ")[1]
        creation_date_converted = self.convert_date_format(creation_date_raw)  # Converte a data


        # Compilando todas as informações em um dicionário
        info = {
            'name': squadron_name,
            'number_of_players': num_players,
            'creation_date': creation_date_converted,
            #'air_targets_destroyed': air_targets_destroyed,
            #'ground_targets_destroyed': ground_targets_destroyed,
            #'deaths': deaths,
            #'flight_time': flight_time,
            #'squadron_rating': squadron_rating,
            #'squadron_activity': squadron_activity
        }
        
        squadron_info.append(info)

        # A estrutura de dados para armazenar informações dos jogadores
        players_info = []

        # Espera garantir que a página tenha sido carregada
        self.web_handler._wait_for_element("//div[@class='squadrons-members__table']", timeout=10)

        # Captura todos os elementos da grid de membros
        members_xpath = "//div[@class='squadrons-members__table']/div[contains(@class, 'squadrons-members__grid-item')]"
        members_elements = self.web_handler.get_elements_by_xpath(members_xpath)

        # Processar em grupos de 6, já que cada jogador ocupa 6 divs consecutivas
        # Process in groups of 6, as each player occupies 6 consecutive divs
        for i in range(6, len(members_elements), 6):
            # O número é o texto do primeiro elemento no bloco de 6 elementos
            number = members_elements[i].text.strip()
            
            # O nome e o link do jogador estão no segundo elemento, que contém a tag <a>
            player_name_elements = web_handler.get_elements_by_tag_from_element(members_elements[i + 1], 'a')
            if player_name_elements:
                player_name_element = player_name_elements[0]  # Assume que existe pelo menos uma tag <a>
                player_name = player_name_element.text.strip()
                player_link = player_name_element.get_attribute('href')
            else:
                player_name = "Name not found"
                player_link = "#"
            
            # A classificação pessoal do esquadrão é o texto do terceiro elemento
            personal_clan_rating = members_elements[i + 2].text.strip()
            
            # A atividade é o texto do quarto elemento
            activity = members_elements[i + 3].text.strip()
            
            # O cargo é o texto do quinto elemento (nota: pode ser oculto em dispositivos móveis)
            role = members_elements[i + 4].text.strip()
            
            # A data de admissão é o texto do sexto elemento (nota: pode ser oculto em dispositivos móveis)
            date_of_entry = members_elements[i + 5].text.strip()
            
            date_of_entry_raw = members_elements[i + 5].text.strip()
            date_of_entry_converted = self.convert_date_format(date_of_entry_raw)

            player_info = {
                'squadron_name': squadron_name,
                'number': number,
                'player_name': player_name,
                'player_link': player_link,
                'personal_clan_rating': personal_clan_rating,
                'activity': activity,
                'role': role,
                'date_of_entry': date_of_entry_converted,
            }
            players_info.append(player_info)
        

        return squadron_info ,players_info

    @staticmethod
    def get_clan_and_player_name(ctx, player_name: str) -> tuple[str, str] | tuple[None, None]:
        clan_name = None  # Define clan_name with a default value
        # If no player name is provided, use the nickname of the user who invoked the command
        if player_name is None:
            full_name = ctx.author.nick
            if not re.match(r'\[\w+\]', full_name):
                return None, None
            clan_name, player_name = full_name.split('] ')
            clan_name = clan_name.replace('[', '').replace(']', '').replace(' ', '')  # Remove os colchetes e espaços

        return clan_name, player_name

    
    async def get_current_tournaments(self) -> list[dict]:
        self.logger.info("Fetching current tournaments.")
        base_url = "https://tss.warthunder.com/index.php?action=current_tournaments"
        
        tournaments_info = []  # Inicializa fora do loop para acumular dados de todos os torneios encontrados
        
        try:
            self.web_handler.open_link(base_url)
            self.logger.info(f"Opened URL: {base_url}")
            
            self.web_handler.click_element("//a[normalize-space()='Tournaments']")
            
            # Define o XPath para selecionar todos os cartões de torneio
            tournaments_xpath = "(//div[@class='card_tournament open'])"

            self.web_handler._wait_for_element(tournaments_xpath)
            
            cards = self.web_handler.get_elements_by_xpath(tournaments_xpath)
            for card in cards:
                tournament_info = {
                'tournament_id': self.web_handler.get_attribute_of_element(card, ".", "tournamentid"),
                'tournament_name': self.web_handler.get_text_on_element(card, ".//div[@class='name_tournament']").strip(),
                'start_date': self.web_handler.get_text_on_element(card, ".//span[@card-name='dayTournament']").strip(),
                'format_team': self.web_handler.get_text_on_element(card, ".//span[@card-name='formatTeam']").strip(),
                'cluster': self.web_handler.get_text_on_element(card, ".//span[@card-name='clusterTournament']").strip(),
                'registration_end': self.web_handler.get_text_on_element(card, ".//span[@card-name='time_left_to_start']").strip(),
                'teams_participating': self.web_handler.get_text_on_element(card, ".//span[@card-name='countTeam']").strip(),
                'tournament_type': self.web_handler.get_attribute_of_element(card, ".//span[@card-name='typeTournament']", "data-original-title").strip(),
                'tournament_schedule': self.web_handler.get_text_on_element(card, ".//span[@card-name='schedulerTournament']").strip(),
                'prize_pool': self.web_handler.get_text_on_element(card, ".//span[@card-name='prize_pool']").strip(),
                # Certifique-se de ajustar os seletores para corresponder à sua estrutura exata de HTML
            }
                tournaments_info.append(tournament_info)
                self.logger.debug("Added tournament info: %s", tournament_info['tournament_name'])
                
                print(tournament_info)
                # Seu código anteriormente tinha uma condição baseada em num_clans, que parece não se aplicar aqui.
                # Se você tiver uma lógica similar para limitar os torneios, adicione-a aqui.
                
        except Exception as e:
            self.logger.error(f"Failed to fetch tournament information: {e}", exc_info=True)
        
        self.logger.info("Successfully fetched tournament information.")
        return tournaments_info


if __name__ == "__main__":
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
        #print(info)

        info = asyncio.run(scraper.get_squadron_leaderboard_info(num_clans=100))
        
        dynamic_data_handler.insert_data('SquadronLeaderboard', info)

        for i in info:
            squadron_info, squadron_players = asyncio.run(scraper.get_squadron_info(i['link']))
            dynamic_data_handler.insert_data('squadroninfo', squadron_info)
            dynamic_data_handler.insert_data('squadronplayers', squadron_players)
        
        logging.info("Data collection and database insertion completed successfully.")

    except json.JSONDecodeError as e:
        logging.error("Failed to parse JSON configuration: %s", e, exc_info=True)
    except Exception as e:
        logging.exception("An unexpected error occurred during the squadron scraping process: %s", e)
    finally:
        browser_handler.close()
        logging.info("Squadron Scraper has finished running.")