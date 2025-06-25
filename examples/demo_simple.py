"""
Demo simples da biblioteca humanlike-automation
Acessa YouTube e demonstra o uso básico

Uso: python demo_simple.py
"""

import sys
import os
import time

# Adicionar o diretório pai ao path para importar a biblioteca
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botinfrastructure import BrowserHandler, WebPageHandler


def demo_youtube():
    """Demo simples: acessa YouTube"""
    print("\n" + "="*50)
    print("🎥 DEMO HUMANLIKE-AUTOMATION")
    print("🎯 Acessando YouTube automaticamente")
    print("="*50)
    
    # Configurar navegador (modo visível para demonstração)
    print("\n🚀 1. Configurando navegador...")
    browser = BrowserHandler(
        site="https://www.youtube.com",
        profile="demo",
        proxy=None,
        profile_folder="./profiles"
    )
    
    try:
        # Iniciar navegador
        print("📱 2. Iniciando navegador...")
        driver = browser.execute()
        web_handler = WebPageHandler(driver)
        
        # Navegar para YouTube
        print("🌐 3. Navegando para YouTube...")
        web_handler.open_link("https://www.youtube.com")
        print("⏳ 4. Aguardando carregamento...")
        time.sleep(4)
        
        # Verificar se carregou
        title = driver.title
        print(f"📄 5. Página carregada: {title}")
        
        # Fechar popup se existir
        print("🍪 6. Verificando popups...")
        try:
            reject_btn = web_handler.get_element_by_xpath("//button[contains(text(), 'Reject all')]")
            if reject_btn:
                reject_btn.click()
                print("   ✅ Popup de cookies fechado")
                time.sleep(2)
            else:
                print("   ℹ️ Nenhum popup encontrado")
        except:
            print("   ℹ️ Nenhum popup para fechar")
        
        # Buscar vídeos
        print("🔍 7. Buscando vídeos na página...")
        videos = web_handler.get_elements_by_xpath("//a[@id='video-title']")
        
        if videos:
            print(f"   ✅ Encontrados {len(videos)} vídeos!")
            
            # Mostrar os primeiros 3 vídeos
            print("\n📺 Primeiros vídeos encontrados:")
            for i, video in enumerate(videos[:3]):
                try:
                    title = video.get_attribute('title') or video.text
                    print(f"   {i+1}. {title[:60]}...")
                except:
                    print(f"   {i+1}. [Título não disponível]")
            
            # Clicar no primeiro vídeo
            print(f"\n▶️ 8. Clicando no primeiro vídeo...")
            first_video = videos[0]
            video_title = first_video.get_attribute('title') or "Vídeo sem título"
            print(f"   🎬 Vídeo: {video_title[:50]}...")
            
            first_video.click()
            
            print("⏳ 9. Aguardando carregamento do vídeo...")
            time.sleep(6)
            
            # Verificar se o vídeo carregou
            try:
                video_player = web_handler.get_element_by_xpath("//video")
                if video_player:
                    print("   ✅ Player de vídeo carregado!")
                    print("   🎵 Vídeo reproduzindo...")
                    
                    # Aguardar 8 segundos assistindo
                    print("   ⏰ Assistindo por 8 segundos...")
                    time.sleep(8)
                    
                    print("\n🎉 DEMO CONCLUÍDA COM SUCESSO!")
                    return True
                else:
                    print("   ❌ Player de vídeo não encontrado")
                    return False
            except Exception as e:
                print(f"   ❌ Erro verificando player: {e}")
                return False
                
        else:
            print("   ❌ Nenhum vídeo encontrado na página")
            return False
            
    except Exception as e:
        print(f"\n❌ ERRO DURANTE EXECUÇÃO: {e}")
        return False
    
    finally:
        print("\n🔚 10. Fechando navegador...")
        try:
            browser.close()
            print("   ✅ Navegador fechado")
        except:
            print("   ⚠️ Erro ao fechar navegador")


def main():
    """Função principal"""
    success = demo_youtube()
    
    print("\n" + "="*50)
    if success:
        print("✅ DEMO EXECUTADA COM SUCESSO!")
        print("🎯 A biblioteca humanlike-automation está funcionando!")
    else:
        print("❌ DEMO FALHOU!")
        print("🔧 Verifique a configuração e tente novamente")
    
    print("\n📚 Próximos passos:")
    print("   • Execute: python youtube_random_player.py")
    print("   • Execute: python youtube_human_behavior.py")
    print("   • Veja mais exemplos na pasta examples/")
    print("="*50)


if __name__ == "__main__":
    main()
