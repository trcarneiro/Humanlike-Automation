"""
Teste simples da implementação stealth
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from botinfrastructure import BrowserHandler, PortableBrowserManager
    print("✓ Import successful")
    
    # Testar criação do manager
    manager = PortableBrowserManager()
    print("✓ PortableBrowserManager created")
    
    # Testar status
    status = manager.get_status()
    print(f"✓ Status: {status}")
    
    # Testar BrowserHandler com stealth
    browser = BrowserHandler.create_stealth_browser("https://example.com")
    print("✓ Stealth browser handler created")
    
    print("\n🎉 All imports and basic functionality working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
