import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from botinfrastructure import WebPageHandler
from data_handler import DataHandler
from selenium.webdriver.support.ui import Select
import os

class LinkedInScreenLogic:
    def __init__(self, web_handler: WebPageHandler):
        self.web_handler = web_handler
        self.db_handler = DataHandler()
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_logged_in(self, user, password):
        try:
            logged = self.web_handler.get_element_by_xpath("(//div[@role='region'])[2]")
            if logged:
                self.logger.info("User is logged in.")
                return True
            else:
                self.logger.info("User is Not logged in.")
                if self.login(user, password):
                    self.logger.info("User logged in successfully.")
                    return True
                else:
                    self.logger.error("Failed to login.")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to check login status: {e}")
            return False
        
    def login(self, username, password):
        try:
            max_attempts = 3  # Definimos o número máximo de tentativas
            attempt = 0
            
            while attempt < max_attempts:
                attempt += 1
                self.logger.info(f"Tentativa de login {attempt}/{max_attempts}")
                
                if not self.web_handler.driver.current_url == "https://www.linkedin.com":
                    self.web_handler.open_link("https://www.linkedin.com")
                
                time.sleep(15)  # Aguardar o carregamento da página
                
                # Verificar se há o botão "Sign in" ou se já está logado
                logged = self.web_handler.get_element_by_xpath("//div[contains(@class,'nav__cta-container order-3')]//a[1]")
                
                if logged:
                    self.logger.info("Usuário não está logado, tentando login.")
                    self.web_handler.open_link("https://www.linkedin.com/login")
                    
                    # Verifica se há o botão "Bem-vindo de volta"
                    xpath = "//div[@class='member-profile-block']//button[1]"
                    welcomeback = self.web_handler.get_element_by_xpath(xpath)
                    if welcomeback:
                        self.logger.info("Usuário já está logado (Bem-vindo de volta).")
                        self.web_handler.click_element(xpath)
                        return True
                    else:
                        # Realiza o login com as credenciais
                        self.web_handler.open_link("https://www.linkedin.com/login")
                        self.web_handler.send_text('//*[@id="username"]', username)
                        self.web_handler.send_text('//*[@id="password"]', password)
                        self.web_handler.click_element('//*[@type="submit"]')
                        time.sleep(5)  # Espera o login ser processado
                        
                        # Verifica se o login foi bem-sucedido
                        if self.web_handler.driver.current_url == "https://www.linkedin.com/feed/":
                            self.logger.info("Login bem-sucedido.")
                            return True
                        else:
                            self.logger.warning("Falha no login, tentando novamente.")
                else:
                    self.logger.info("Usuário já está logado.")
                    return True

                # Atualizar a página e tentar novamente
                self.logger.info("Atualizando a página para tentar novamente.")
                self.web_handler.driver.refresh()
                time.sleep(5)

            # Se todas as tentativas falharem
            self.logger.error(f"Login falhou após {max_attempts} tentativas.")
            return False

        except Exception as e:
            self.logger.error(f"Falha ao realizar o login: {e}")
            return False
        
    def set_language(self, language):
        try:
            self.web_handler.click_element('//img[@class="global-nav__me-photo evi-image ember-view"]')
            self.web_handler.click_element(f'//button[normalize-space(text())="{language}"]')
            self.logger.info("Language set successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to set language: {e}")
            return    
        
    def search_bar_filter(self, search_term = 'python', location='Brazil'):
        
        try:
            self.web_handler.click_element("//span[@title='Jobs']")
            self.web_handler.send_text('//input[@aria-label="Search by title, skill, or company"][1]', search_term)
            self.web_handler.send_text('//input[@aria-label="City, state, or zip code"][1]', location)
            
            time.sleep(5)
            self.web_handler.send_keys()
        except Exception as e:
            self.logger.error(f"Failed to search for jobs: {e}")
            return False
        
    def get_filters(self, filter_id):
        """Retrieve filters associated with the given keyword from the database."""
        try:
            filters = self.db_handler.get_filters_by_criteria(filter_id=filter_id)
            if not filters:
                self.logger.warning(f"No filters found for id: '{id}'.")
                return []
            self.logger.info(f"Retrieved {len(filters)} filters for keyword: '{id}'.")
            return filters
        except Exception as e:
            self.logger.error(f"Error retrieving filters for keyword '{id}': {e}")
            return []

    def apply_filters_on_screen(self, filters):
        try:
            self.web_handler.click_element("(//button[normalize-space()='All filters'])[1]")
            self.logger.info("Clicked on 'All filters' button.")

            for filter_item in filters:
                filter_type = filter_item.filter_type
                filter_value = filter_item.filter_value

                self.logger.info(f"Applying filter: '{filter_type}' with value '{filter_value}'.")

                if filter_type == "location":
                    self.apply_location_filter(filter_value)
                elif filter_type == "job_type":
                    self.apply_job_type_filter(filter_value)
                elif filter_type == "experience_level":
                    self.apply_experience_level_filter(filter_value)
                elif filter_type == "date_posted":
                    self.apply_date_posted_filter(filter_value)
                elif filter_type == "salary":
                    self.apply_salary_filter(filter_value)
                elif filter_type == "company":
                    self.apply_company_filter(filter_value)
                elif filter_type == "industry":
                    self.apply_industry_filter(filter_value)
                elif filter_type == "easyapply":
                    self.apply_easy_apply_filter(filter_value)
                else:
                    self.logger.warning(f"Unknown filter type: '{filter_type}'")

            # After applying all filters, click the 'Show results' button
            self.web_handler.click_element("(//div[contains(@class,'justify-flex-end display-flex')])//span[@class='artdeco-button__text' and starts-with(normalize-space(.), 'Show')]")
            self.logger.info("Clicked 'Show results' button after applying filters.")

            return True
        except Exception as e:
            self.logger.error(f"Error applying filters: {e}")
        return False

    def apply_location_filter(self, value):
            
        if value == "On-Site":
            xpath = "//label[@for='advanced-filter-locationType-1']"
        elif value == "Remote":
            xpath = "//label[@for='advanced-filter-workplaceType-2']"
        elif value == "Hybrid":
            xpath = "//label[@for='advanced-filter-workplaceType-3']"
        else:
            xpath = f"//input[@placeholder='Add a location']"
            self.web_handler.send_text(xpath, value)
        return self.web_handler.click_element(xpath)

    def apply_job_type_filter(self, value):
        xpath_map = {
        "Full-time": "//label[@for='advanced-filter-timeType-F']",
        "Part-time": "//label[@for='advanced-filter-timeType-P']",
        "Contract": "//label[@for='advanced-filter-timeType-C']",
        "Temporary": "//label[@for='advanced-filter-timeType-T']",
        "Volunteer": "//label[@for='advanced-filter-timeType-V']",
        "Internship": "//label[@for='advanced-filter-timeType-I']",
        "Other": "//label[@for='advanced-filter-timeType-O']"
        }
        xpath = xpath_map.get(value)
        if xpath:
            self.web_handler.click_element(xpath)

    def apply_experience_level_filter(self, value):
        xpath_map = {
        "Internship": "//label[@for='advanced-filter-experience-1']",
        "Entry level": "//label[@for='advanced-filter-experience-2']",
        "Associate": "//label[@for='advanced-filter-experience-3']",
        "Mid-Senior level": "//label[@for='advanced-filter-experience-4']",
        "Director": "//label[@for='advanced-filter-experience-5']",
        "Executive": "//label[@for='advanced-filter-experience-6']"
        }
        xpath = xpath_map.get(value)
        if xpath:
            self.web_handler.click_element(xpath)

    def apply_date_posted_filter(self, value):
        xpath_map = {
        "Any time": "//label[@for='advanced-filter-timePostedRange-r0']",
        "Past month": "//label[@for='advanced-filter-timePostedRange-r2592000']",
        "Past week": "//label[@for='advanced-filter-timePostedRange-r604800']",
        "Past 24 hours": "//label[@for='advanced-filter-timePostedRange-r86400']"
        }
        xpath = xpath_map.get(value)
        if xpath:
            self.web_handler.click_element(xpath)

    def apply_salary_filter(self, value):
        # This might need a more complex implementation depending on how LinkedIn's salary filter works
        xpath = "//button[@aria-label='Salary filter. Clicking this button displays all Salary filter options.']"
        self.web_handler.click_element(xpath)
        # Additional logic to set the salary range would go here

    def apply_company_filter(self, value):
        xpath = "//input[@placeholder='Add a company']"
        self.web_handler.send_text(xpath, value)

    def apply_industry_filter(self, value):
        xpath = "//input[@placeholder='Add an industry']"
        self.web_handler.send_text(xpath, value)

    def apply_easy_apply_filter(self, value):
        if value.lower() == "on":
            xpath = "(//div[@data-control-name='filter_detail_select'])[1]"
            self.web_handler.go_to_element(xpath)
            self.web_handler.click_element(xpath)
                        
    def search_jobs(self, keyword, filter):
        try:
            
            
            #self.is_logged_in()
            #self.web_handler.open_link(f"https://www.linkedin.com/jobs/search/?keywords={keyword}")
            self.search_bar_filter(keyword)
            time.sleep(5)  # Aguardando o carregamento da página

            all_jobs = []
            max_jobs_to_collect = 1  # Set this to the number of jobs you want to collect for testing
            job_count = 0
            
            # Retrieve and apply filters for the keyword
            filters = self.get_filters(2)
            if filters:
                self.apply_filters_on_screen(filters)
                time.sleep(5)  # Wait for the filters to be 
            else:
                self.logger.warning("No filters found for the keyword.")

            self.logger.info("Filters {}")

            while job_count < max_jobs_to_collect:
                jobs = self.web_handler.get_elements_by_xpath("//li[contains(@class, 'jobs-search-results__list-item')]")
                self.logger.info(f"Found {len(jobs)} job listings on the current page.")

                for job in jobs:
                    details = self.get_job_details(job)
                    if details:
                        all_jobs.append(details)
                        job_count += 1
                        if job_count >= max_jobs_to_collect:
                            break  # Exit the loop once we've collected enough jobs

                # Exit the outer loop if we have collected the desired number of jobs
                if job_count >= max_jobs_to_collect:
                    break

                # Optionally, navigate to the next page
                self.go_to_next_page()

            return all_jobs
        except Exception as e:
            self.logger.error(f"Failed to search jobs: {e}")
            return []

    def get_job_details(self, job_element):
        try:
            # Click on the job element to open the job details
            job_element.click()
            time.sleep(2)  # Wait for the page to load
            
            # Extract job details
            job_details = {
                'title': self.web_handler.get_text_by_xpath("//div[@class='jobs-search__job-details--wrapper']//h1"),
                'link': self.web_handler.get_attribute_by_xpath("(//div[@class='display-flex justify-space-between flex-wrap mt2'])[1]//h1//a", "href")
                #'company': self.web_handler.get_text_by_xpath("//a[@data-tracking-control-name='public_jobs_topcard-org-name']"),
                #'location': self.web_handler.get_text_by_xpath("//span[@class='jobs-unified-top-card__bullet']"),
                #'job_type': self.web_handler.get_text_by_xpath("//ul[contains(@class, 'jobs-unified-top-card__job-insight')]//li[1]"),  # Adjust this XPath as needed
                #'date_posted': self.web_handler.get_text_by_xpath("//span[@class='jobs-unified-top-card__posted-date']"),
                #'job_url': self.web_handler.driver.current_url,
                #'description': self.web_handler.get_text_by_xpath("//div[@class='jobs-description__content']"),
                #'job_function': self.web_handler.get_text_by_xpath("//span[@class='jobs-box__group-title'][contains(text(), 'Job function')]/following-sibling::span"),
                #'company_industry': self.web_handler.get_text_by_xpath("//span[@class='jobs-box__group-title'][contains(text(), 'Industries')]/following-sibling::span"),
                #'min_amount': self.extract_salary("//span[contains(text(), 'Minimum pay')]"),
                #'max_amount': self.extract_salary("//span[contains(text(), 'Maximum pay')]"),
                #'currency': self.extract_currency("//span[contains(text(), 'Minimum pay')]"),
                #'is_remote': self.check_remote("//span[@class='jobs-unified-top-card__workplace-type']"),
            }

            # Log the retrieved job details
            #self.logger.info(f"Retrieved details for job: {job_details['title']} at {job_details['company']}")
            
            # Optionally close the job details panel
            #self.web_handler.click_element("//button[@aria-label='Close']")
            
            return job_details
        
        except Exception as e:
            self.logger.error(f"Failed to retrieve job details: {e}")
            return {}

    # Helper functions
    def extract_salary(self, xpath):
        try:
            salary_text = self.web_handler.get_text_by_xpath(xpath)
            # Parse the salary text to extract the numerical value
            salary = float(salary_text.replace(',', '').replace('$', '').strip()) if salary_text else None
            return salary
        except Exception as e:
            self.logger.error(f"Failed to extract salary: {e}")
            return None

    def extract_currency(self, xpath):
        try:
            salary_text = self.web_handler.get_text_by_xpath(xpath)
            # Extract the currency symbol from the salary text (assuming $ for USD)
            currency = 'USD' if '$' in salary_text else None
            return currency
        except Exception as e:
            self.logger.error(f"Failed to extract currency: {e}")
            return None

    def check_remote(self, xpath):
        try:
            remote_text = self.web_handler.get_text_by_xpath(xpath)
            return 'remote' in remote_text.lower()
        except Exception as e:
            self.logger.error(f"Failed to check if job is remote: {e}")
            return False

    def go_to_next_page(self, total_pages=1):
        try:
            wait = WebDriverWait(self.web_handler.driver, 10)  # Adjust the wait time as necessary

            for page_number in range(2, total_pages + 1):  # Start from page 2 to the specified total pages
                try:
                    right_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list")))

                    self.web_handler.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", right_frame)
                    time.sleep(3)  # Small pause to ensure the page loads correctly

                    next_btn_selector = f"button[aria-label='Page {page_number}']"
                    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_btn_selector)))

                    if next_btn.location_once_scrolled_into_view:
                        next_btn.click()
                        self.logger.info(f"Clicked on the Page {page_number} button.")
                    else:
                        self.logger.error(f"Page {page_number} button is not visible in the viewport.")
                        return False

                except Exception as e:
                    self.logger.error(f"Failed to find or click the Page {page_number} button: {e}")
                    return False
        except Exception as e:
            self.logger.error(f"Failed to navigate to the next page: {e}")
            return False

    def close(self):
        self.web_handler.close()

    async def easy_apply(self, job_link, user, resume_path):
        try:
            self.logger.info(f"Opening job link: {job_link}")
            self.web_handler.open_link(job_link)
            time.sleep(2)  # Adding a short delay to ensure the page loads
        except Exception as e:
            self.logger.error(f"Failed to open job link: {job_link}. Error: {e}")
            return False

        try:
            self.logger.info("Attempting to click the Easy Apply button.")
            self.web_handler.click_element("(//span[@class='artdeco-button__text'][normalize-space()='Easy Apply'])[2]")
            self.logger.info("Easy Apply button clicked successfully.")
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"Failed to click the Easy Apply button. Error: {e}")
            return False

        try:
            phone_number_input_xpath = "(//input[@class=' artdeco-text-input--input'])"
            self.logger.warning(f"Entering phone number: {user.cell_phone}")
            self.web_handler.send_text(phone_number_input_xpath, user.cell_phone)
            self.logger.warning("Phone number entered successfully.")
            time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Failed to enter phone number. Error: {e}")
            return False

        try:
            self.logger.info("Attempting to click the Next button.")
            self.web_handler.click_element("//span[normalize-space()='Next']")
            self.logger.info("Next button clicked successfully.")
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"Failed to click the Next button. Error: {e}")
            return False

        # Upload resume
        try:
            self.logger.info("Attempting to upload resume.")
            file_input_xpath = "//input[@type='file']"
            absolute_resume_path = os.path.abspath(resume_path)
            self.web_handler.upload_file(file_input_xpath, absolute_resume_path)
            self.logger.info(f"Resume uploaded successfully from path: {resume_path}")  
            self.web_handler.click_element('//*[@aria-label="Continue to next step"]')
        except Exception as e:
            self.logger.error(f"Failed to upload resume. Error: {e}")
            return False
        
        # Attempt to fill additional questions
        try:
            self.logger.info("Attempting to capture and fill additional questions.")
            if not await self.capture_and_fill_questions(user):
                self.logger.error("Failed to capture and fill additional questions.")
                return False
            
            self.logger.info("Attempting to click the Submit application button.")
            self.web_handler.click_element("//span[normalize-space()='Review']")
            self.logger.info("Submit application button clicked successfully.")

            self.logger.info("Attempting to click the Submit application button.")
            self.web_handler.click_element("//span[normalize-space()='Submit application']")
            self.logger.info("Submit application button clicked successfully.")
            
            # Record the application in the database
            self.record_application_in_database(jobid=self.get_job_id(job_link), userid=userid)
                    
        except Exception as e:
            self.logger.error(f"Failed to click the Submit application button. Error: {e}")
            return False

    def fill_response(self, label_element, answer_text):
        """Preenche a resposta no campo de entrada correspondente na página da web."""
        try:
            if not answer_text or answer_text is None:
                self.logger.warning(f"Resposta inválida ou 'None' fornecida para a pergunta '{label_element.text.strip()}'. Pulando preenchimento.")
                return

            input_id = label_element.get_attribute('for')
            if not input_id:
                self.logger.warning(f"Sem campo de entrada associado ao rótulo '{label_element.text.strip()}'.")
                return

            input_element = self.web_handler.driver.find_element(By.ID, input_id)
            if input_element is None:
                self.logger.error(f"Elemento de entrada não encontrado para a pergunta '{label_element.text.strip()}'.")
                return

            tag_name = input_element.tag_name.lower()

            if tag_name == 'input':
                input_type = input_element.get_attribute('type').lower()
                if input_type in ['text', 'email', 'number', 'tel', 'url']:
                    input_element.clear()
                    input_element.send_keys(answer_text)
                elif input_type == 'radio':
                    radio_button = self.web_handler.driver.find_element(By.XPATH, f"//input[@type='radio' and @value='{answer_text}']")
                    if radio_button:
                        radio_button.click()
                elif input_type == 'checkbox':
                    if answer_text.lower() in ['yes', 'true']:
                        if not input_element.is_selected():
                            input_element.click()
                    else:
                        if input_element.is_selected():
                            input_element.click()
            elif tag_name == 'textarea':
                input_element.clear()
                input_element.send_keys(answer_text)
            elif tag_name == 'select':
                select = Select(input_element)
                try:
                    select.select_by_visible_text(answer_text)
                    self.logger.info(f"Opção '{answer_text}' selecionada no dropdown para a pergunta '{label_element.text.strip()}'.")
                except Exception as e:
                    self.logger.error(f"Falha ao selecionar '{answer_text}' no dropdown para a pergunta '{label_element.text.strip()}': {e}")
            else:
                self.logger.warning(f"Tipo de entrada '{tag_name}' não tratado para a pergunta '{label_element.text.strip()}'.")
        except Exception as e:
            self.logger.error(f"Falha ao preencher a resposta para a pergunta '{label_element.text.strip()}': {e}")

    async def capture_and_fill_questions(self, user):
        """Função principal para capturar e preencher todas as perguntas."""
        try:
            self.logger.info("Capturando todas as perguntas adicionais e campos de entrada.")

            # Localizar todos os rótulos de perguntas
            label_elements = self.web_handler.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'jobs-easy-apply-form-element')]//label"
            )

            for label in label_elements:
                question_text = self.clean_question_text(label.text.strip())
                if not question_text:
                    continue 

                self.logger.info(f"Processando pergunta: '{question_text}'")

                # Use get_questions_by_criteria to get the question data from the database
                question_data = self.db_handler.get_questions_by_criteria(question_text=question_text)

                if question_data:
                    question = question_data[0]  # Assuming you get a list of dictionaries, take the first match
                    question_id = question['id']
                    self.logger.info(f"Pergunta '{question_text}' já existe no banco de dados com ID: {question_id}.")

                    # Get the response for this question and the default user ID
                    response = self.db_handler.get_response_by_question_and_user(question_id, user.id)
                    
                    # Assuming question has an ID or some identifier
                    self.record_question_response_in_database(applyjobid=self.get_current_apply_job_id(), questionid=question.id, response=response)
            
                    if response:
                        self.fill_response(label, response)
                    else:
                        self.logger.warning(f"Resposta não encontrada no banco de dados para a pergunta '{question_text}'.")
                else:
                    # Handle the case where the question is not in the database
                    self.logger.info(f"Nova pergunta não encontrada no banco de dados, inserindo: '{question_text}'")
                    new_question_data = self.get_question_data(label)
                    self.insert_question_if_not_exists(new_question_data)

            self.logger.info("Concluído o processamento de todas as perguntas da aplicação.")
            return True
        except Exception as e:
            self.logger.error(f"Ocorreu um erro ao processar as perguntas: {e}")
            return False

    def get_question_data(self, label_element):
        """Determina o tipo de pergunta e possíveis respostas."""
        try:
            input_element = self.web_handler.driver.find_element(By.ID, label_element.get_attribute('for'))
            input_tag_name = input_element.tag_name.lower()
            input_type = input_element.get_attribute('type').lower() if input_tag_name == 'input' else None

            if input_tag_name == 'select':
                type_of_question = 'multiple choice'
                possible_responses = [option.text.strip() for option in input_element.find_elements(By.TAG_NAME, "option") if option.text.strip()]
            elif input_tag_name == 'input' and input_type == 'radio':
                type_of_question = 'radio'
                possible_responses = [elem.get_attribute('value').strip() for elem in input_element.find_elements(By.NAME, input_element.get_attribute("name")) if elem.get_attribute('value').strip()]
            elif input_tag_name == 'input' and input_type in ['text', 'email', 'number', 'tel', 'url']:
                type_of_question = 'text'
                possible_responses = []
            elif input_tag_name == 'textarea':
                type_of_question = 'textarea'
                possible_responses = []
            elif input_tag_name == 'input' and input_type == 'checkbox':
                type_of_question = 'checkbox'
                possible_responses = [input_element.get_attribute('value').strip()]
            else:
                type_of_question = 'unknown'
                possible_responses = []
                self.logger.warning(f"Tipo de entrada '{input_tag_name}' não tratado para a pergunta '{label_element.text.strip()}'.")

            required = label_element.find_element(By.XPATH, "..").get_attribute("aria-required") == "true"

            return {
                'question_text': label_element.text.strip(),
                'type_of_question': type_of_question,
                'required': required,
                'possible_responses': possible_responses
            }
        except Exception as e:
            self.logger.error(f"Erro ao determinar o tipo de pergunta: {e}")
            return None

    def insert_question_if_not_exists(self, question_data):
        """Insere a pergunta no banco de dados se ela não existir."""
        try:
            # Certifique-se de que 'question_text' está presente em question_data
            question_text = question_data.get('question_text')
            question_text = self.clean_question_text(question_text)
            if question_text:
                existing_question = self.db_handler.get_questions_by_criteria(question_text=question_text)
                if not existing_question:
                    self.db_handler.insert_question(
                        question_text=question_text,
                        type_of_question=question_data.get('type_of_question'),
                        required=question_data.get('required'),
                        possible_responses=question_data.get('possible_responses')
                    )
                    #TODO -  Return ID of the inserted question
                    return False
                
                return existing_question
            
            else:
                self.logger.error("Dados da pergunta inválidos: 'question_text' está ausente.")
        except Exception as e:
            self.logger.error(f"Erro ao inserir a pergunta no banco de dados: {e}")

    def clean_question_text(self, question_text):
        """Remove duplicate content after the question mark or period and trim quotes."""
        clean_text = question_text.split("?")[0].strip().strip("'")
        if len(clean_text) < len(question_text):
            clean_text += "?"  # Add the question mark back if it was removed
        return clean_text

    def record_application_in_database(self, jobid, userid):
        """Records the job application in the database."""
        try:
            new_apply_job = ApplyJob(jobid=jobid, userid=userid)
            self.session.add(new_apply_job)
            self.session.commit()
            self.logger.info(f"Recorded application for job {jobid} by user {userid}.")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Failed to record application. Error: {e}")