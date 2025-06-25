"""
Teste prático do modo stealth - execução rápida
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botinfrastructure import BrowserHandler

def main():
    print("🔒 Testando modo stealth...")
    
    try:
        # Criar browser stealth
        browser = BrowserHandler.create_stealth_browser(
            site="https://httpbin.org/headers",
            profile="test_quick",
            headless=True  # Modo headless para teste rápido
        )
        
        print("✓ Browser stealth criado")
        
        # Verificar status
        status = browser.get_portable_browser_status()
        print(f"Chrome disponível: {status['chrome_available']}")
        
        # Executar
        driver = browser.execute()
        print("✓ Driver inicializado")
        
        # Teste básico
        driver.get("https://httpbin.org/headers")
        title = driver.title
        print(f"✓ Página carregada: {title}")
        
        # Verificar se webdriver está oculto
        webdriver_detected = driver.execute_script("return navigator.webdriver")
        print(f"WebDriver detectado: {webdriver_detected}")
        
        # Fechar
        browser.close()
        print("✓ Browser fechado")
        
        print("\n🎉 Teste stealth concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
