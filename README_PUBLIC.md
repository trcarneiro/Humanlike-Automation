# Human-Like Automation Library

Uma biblioteca Python para automação de navegador que simula comportamento humano natural.

## 🚀 **Características Principais**

- **Simulação Humana**: Delays aleatórios, movimentos naturais de mouse, padrões de digitação realistas
- **Gerenciamento de Sessões**: Múltiplas sessões de navegador isoladas
- **Configuração Flexível**: XPaths e credenciais em arquivos de configuração
- **Anti-Detecção**: Técnicas para evitar detecção de bot
- **Logging Avançado**: Sistema de logs detalhado para debugging

## 📦 **Instalação**

```bash
pip install humanlike-automation
```

## ⚙️ **Configuração**

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do seu projeto:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_db_password_here
DB_NAME=your_database_name

# OpenAI Configuration (opcional)
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. XPaths Configuráveis

Os XPaths são armazenados em `xpaths_config.json`. Você pode customizar para seus sites:

```json
{
  "linkedin": {
    "login": {
      "username_field": "//*[@id='username']",
      "password_field": "//*[@id='password']",
      "submit_button": "//*[@type='submit']"
    }
  },
  "seu_site": {
    "categoria": {
      "elemento": "//xpath/para/elemento"
    }
  }
}
```

## 🎯 **Uso Básico**

### Automação Simples

```python
from humanlike_automation import BrowserHandler, WebPageHandler

# Inicializar o navegador
browser = BrowserHandler(
    site="https://exemplo.com",
    profile="perfil1",
    proxy=None,
    profile_folder="./profiles"
)

# Obter driver
driver = browser.execute()

# Handler para interações
web_handler = WebPageHandler(driver)

# Navegar e interagir
web_handler.open_link("https://exemplo.com")
web_handler.send_text_humanlike("//input[@id='search']", "texto para pesquisar")
web_handler.click_element_humanlike("//button[@type='submit']")

# Fechar
browser.close()
```

### Gerenciamento de Múltiplas Sessões

```python
from humanlike_automation import BrowserSessionManager

# Criar gerenciador
session_manager = BrowserSessionManager(max_instances=3)

# Inicializar sessão
session = await session_manager.initialize_session(
    site="https://exemplo.com",
    profile="perfil1",
    proxy=None,
    profile_folder="./profiles"
)

# Usar a sessão
if session:
    web_handler = session['handler']
    web_handler.open_link("https://exemplo.com")
    
# Fechar todas as sessões
await session_manager.close_all_sessions()
```

### Usando Configurações

```python
from humanlike_automation import config_manager

# Obter XPath configurável
xpath = config_manager.get_xpath('linkedin', 'login', 'username_field')

# Obter configuração do banco
db_config = config_manager.get_database_config()

# Obter configuração do Telegram
telegram_config = config_manager.get_telegram_config()
```

## 🧠 **Recursos Avançados**

### 1. Delays Humanizados

```python
# Delay aleatório entre 1-3 segundos
await browser._random_sleep(1, 3)

# Delay baseado em contexto
web_handler.human_delay("typing")  # Delay para digitação
web_handler.human_delay("clicking")  # Delay para cliques
web_handler.human_delay("reading")   # Delay para leitura
```

### 2. Padrões de Digitação Naturais

```python
# Digitação com padrões humanos
web_handler.send_text_humanlike(
    xpath="//input[@id='email']",
    text="usuario@email.com",
    typing_speed="normal",  # slow, normal, fast
    mistakes_probability=0.05  # 5% chance de erros
)
```

### 3. Movimentos de Mouse Naturais

```python
# Mover mouse em curva natural até elemento
web_handler.move_to_element_naturally("//button[@id='submit']")

# Scroll natural da página
web_handler.scroll_naturally(direction="down", intensity="medium")
```

### 4. Sistema de Logging

```python
import logging
from humanlike_automation import Utility

# Configurar logger customizado
logger = Utility().setup_logger("meu_bot", "logs/meu_bot.log")

# Usar em suas automações
logger.info("Iniciando automação")
logger.error("Erro encontrado", exc_info=True)
```

## 🔧 **Configurações de Navegador**

### Perfis Personalizados

```python
browser = BrowserHandler(
    site="https://exemplo.com",
    profile="linkedin_profile",  # Nome do perfil
    proxy="127.0.0.1:8080",     # Proxy opcional
    profile_folder="./profiles", # Pasta de perfis
    user_agent="custom_agent"    # User agent customizado
)
```

### Opções Avançadas

```python
# Configurar opções específicas do Chrome
options = browser._initialize_webdriver_options()
options.add_argument("--disable-images")  # Desabilitar imagens
options.add_argument("--mute-audio")      # Sem áudio

# Usar configurações personalizadas
browser.chrome_options = options
driver = browser.execute()
```

## 🤖 **Integração com IA**

### Análise de Páginas com IA

```python
from humanlike_automation import WebpageAnalyzer

analyzer = WebpageAnalyzer()

# Analisar página atual
insights = analyzer.analyze_page(driver.page_source)

# Extrair informações específicas
data = analyzer.extract_structured_data(
    html_content=driver.page_source,
    target_elements=["titles", "prices", "links"]
)
```

### Bot do Telegram (Opcional)

```python
from humanlike_automation import TelegramBotHandler

# Configurar bot (usa credenciais do .env)
bot = TelegramBotHandler()

# Enviar notificações
await bot.send_message("Automação iniciada!")

# Solicitar entrada do usuário
auth_code = await bot.request_auth_code()
```

## 📊 **Monitoramento e Logs**

### Logs Estruturados

```python
# Os logs são salvos automaticamente em:
# - logs/BrowserHandler.log
# - logs/WebPageHandler.log  
# - logs/BrowserSessionManager.log

# Configurar nível de log
import logging
logging.getLogger('humanlike_automation').setLevel(logging.DEBUG)
```

### Métricas de Performance

```python
# Rastrear tempo de execução
start_time = time.time()

# Sua automação aqui...

execution_time = time.time() - start_time
logger.info(f"Automação concluída em {execution_time:.2f} segundos")
```

## 🛡️ **Melhores Práticas**

### 1. **Evitar Detecção**
```python
# Usar delays aleatórios
await browser._random_sleep(2, 5)

# Variar padrões de comportamento
web_handler.random_scroll()
web_handler.random_mouse_movement()

# Usar user agents rotativos
browser.rotate_user_agent()
```

### 2. **Gerenciamento de Recursos**
```python
# Sempre fechar sessões
try:
    # Sua automação...
    pass
finally:
    browser.close()
    await session_manager.close_all_sessions()
```

### 3. **Tratamento de Erros**
```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    element = web_handler.wait_for_element("//button[@id='submit']", timeout=10)
    web_handler.click_element_safely("//button[@id='submit']")
except TimeoutException:
    logger.error("Elemento não encontrado dentro do tempo limite")
except NoSuchElementException:
    logger.error("Elemento não existe na página")
```

## 🚀 **Exemplos Avançados**

### Automação de Login Multi-Etapas

```python
async def automated_login(username, password):
    browser = BrowserHandler(site="https://exemplo.com", profile="login_profile")
    driver = browser.execute()
    web_handler = WebPageHandler(driver)
    
    try:
        # Navegar para página de login
        web_handler.open_link("https://exemplo.com/login")
        
        # Aguardar formulário carregar
        web_handler.wait_for_element(config_manager.get_xpath('site', 'login', 'username_field'))
        
        # Preencher credenciais com delays naturais
        web_handler.send_text_humanlike(
            config_manager.get_xpath('site', 'login', 'username_field'), 
            username
        )
        
        await browser._random_sleep(1, 2)
        
        web_handler.send_text_humanlike(
            config_manager.get_xpath('site', 'login', 'password_field'), 
            password
        )
        
        # Clicar em submit
        web_handler.click_element_humanlike(
            config_manager.get_xpath('site', 'login', 'submit_button')
        )
        
        # Verificar sucesso do login
        success = web_handler.wait_for_element(
            config_manager.get_xpath('site', 'dashboard', 'indicator'),
            timeout=10
        )
        
        return success is not None
        
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        return False
    finally:
        browser.close()
```

### Scraping com Resistência

```python
async def resilient_scraping(urls):
    session_manager = BrowserSessionManager(max_instances=2)
    results = []
    
    for url in urls:
        session = await session_manager.initialize_session(
            site=url,
            profile=f"scraper_{len(results)}",
            proxy=get_rotating_proxy(),  # Função personalizada
            profile_folder="./scraper_profiles"
        )
        
        if session:
            web_handler = session['handler']
            
            try:
                web_handler.open_link(url)
                
                # Aguardar carregamento
                web_handler.wait_for_element("//body", timeout=15)
                
                # Extrair dados
                data = extract_page_data(web_handler)  # Função personalizada
                results.append(data)
                
                # Delay entre requisições
                await asyncio.sleep(random.uniform(3, 7))
                
            except Exception as e:
                logger.error(f"Erro ao scraping {url}: {e}")
                
    await session_manager.close_all_sessions()
    return results
```

## 🔗 **Links Úteis**

- [Documentação Selenium](https://selenium-python.readthedocs.io/)
- [Seletores XPath](https://www.w3schools.com/xml/xpath_syntax.asp)
- [ChromeDriver](https://chromedriver.chromium.org/)

## 📝 **Licença**

MIT License - veja o arquivo LICENSE para detalhes.

## 🤝 **Contribuindo**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ **Disclaimer**

Esta biblioteca deve ser usada responsavelmente e em conformidade com os termos de serviço dos sites que você está automatizando. O desenvolvedor não se responsabiliza pelo uso inadequado desta ferramenta.
