import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# YENİLENMİŞ KANAL LİSTESİ VE KAYNAKLARI
CHANNEL_CONFIG = {
    "Haber": {
        "cnn": "https://www.cnnturk.com/canli-yayin",
        "haberturk": "https://www.haberturk.com/canliyayin",
        "ntv": "https://www.ntv.com.tr/canli-yayin", # tvkulesi yerine doğrudan kendi sitesi
        "trthaber": "https://www.trthaber.com/canli-yayin-izle.html"
    },
    "Spor": {
        "Tivibu Spor": "https://www.tivibuspor.com.tr/canli-yayin",
        "aspor": "https://www.aspor.com.tr/webtv/canli-yayin",
        "HT SPOR": "https://www.haberturk.com/ht-spor-canli-izle"
    },
    "Genel": {
        "now": "https://www.nowtv.com.tr/canli-yayin",
        "tv8": "https://www.tv8.com.tr/canli-yayin",
        "kanald": "https://www.kanald.com.tr/canli-yayin",
        "atv": "https://www.atv.com.tr/canli-yayin"
    }
}

def fetch_link(channel_name, target_url):
    print(f">>> {channel_name.upper()} aranıyor: {target_url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # GitHub'ı gerçek bir Windows Chrome gibi gösterelim
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(30)
        driver.get(target_url)
        
        # Bazı siteler geç açılır, biraz sabır
        time.sleep(15) 
        
        logs = driver.get_log('performance')
        for entry in logs:
            try:
                message = json.loads(entry['message'])['message']
                if 'Network.requestWillBeSent' in message['method']:
                    url = message.get('params', {}).get('request', {}).get('url', '')
                    # M3U8 veya Master playlist yakala
                    if '.m3u8' in url and not any(x in url.lower() for x in ["ads", "analytics", "doubleclick", "pixel"]):
                        print(f"Buldum! -> {channel_name}")
                        driver.quit()
                        return url
            except:
                continue
    except Exception as e:
        print(f"Hata ({channel_name}): {e}")
    finally:
        if driver:
            driver.quit()
    return None

def main():
    m3u_output = "#EXTM3U\n"
    for category, channels in CHANNEL_CONFIG.items():
        for name, url in channels.items():
            live_url = fetch_link(name, url)
            if live_url:
                m3u_output += f'#EXTINF:-1 group-title="{category}",{name.upper()}\n'
                m3u_output += f'{live_url}\n'
            else:
                m3u_output += f'#EXTINF:-1 group-title="{category}",{name.upper()} (YENILENEMEDI)\n'
                m3u_output += f'{url}\n'

    with open("yayin_listesi.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print("İşlem bitti.")

if __name__ == "__main__":
    main()
