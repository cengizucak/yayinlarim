import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Senin IntelliJ'deki kanal listen
CHANNEL_CONFIG = {
    "Haber": {
        "cnn": "https://www.cnnturk.com/canli-yayin",
        "haberturk": "https://www.haberturk.com/canliyayin",
        "ntv": "https://amp.tvkulesi.com/ntv",
        "trthaber": "https://www.trthaber.com/canli-yayin-izle.html"
    },
    "Spor": {
        "Tivibu Spor": "https://amp.tvkulesi.com/tivibu-spor",
        "aspor": "https://amp.tvkulesi.com/a-spor",
        "HT SPOR": "https://amp.tvkulesi.com/ht-spor"
    },
    "Genel": {
        "now": "https://www.nowtv.com.tr/canli-yayin",
        "tv8": "https://amp.tvkulesi.com/tv8",
        "kanald": "https://amp.tvkulesi.com/kanal-d",
        "atv": "https://amp.tvkulesi.com/atv"
    }
}

def fetch_link(channel_name, target_url):
    print(f">>> {channel_name.upper()} için canlı link aranıyor...")
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(target_url)
        time.sleep(12) # Linkin düşmesi için bekliyoruz
        
        logs = driver.get_log('performance')
        for entry in logs:
            message = json.loads(entry['message'])['message']
            if 'Network.requestWillBeSent' in message['method']:
                url = message.get('params', {}).get('request', {}).get('url', '')
                if '.m3u8' in url and not any(x in url for x in ["ads", "analytics"]):
                    print(f"BAŞARILI: {channel_name} bulundu.")
                    driver.quit()
                    return url
        driver.quit()
    except Exception as e:
        print(f"Hata oluştu ({channel_name}): {e}")
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
                # Bulamazsa yedek olarak ana linki koy (TiviMate hata verebilir ama liste bozulmaz)
                m3u_output += f'#EXTINF:-1 group-title="{category}",{name.upper()} (YENILENEMEDI)\n'
                m3u_output += f'{url}\n'

    with open("yayin_listesi.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print("İşlem tamamlandı! yayin_listesi.m3u güncellendi.")

if __name__ == "__main__":
    main()
