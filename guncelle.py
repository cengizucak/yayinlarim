import requests

# IntelliJ'deki channels.py dosyanın içeriği burası
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

def liste_olustur():
    m3u_icerik = "#EXTM3U\n"
    
    for kategori, kanallar in CHANNEL_CONFIG.items():
        for kanal_adi, url in kanallar.items():
            # TiviMate'te kategorize görünmesi için group-title ekliyoruz
            m3u_icerik += f'#EXTINF:-1 group-title="{kategori}",{kanal_adi.upper()}\n'
            m3u_icerik += f'{url}\n'
    
    with open("yayin_listesi.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    print("Liste senin channels.py dosyana göre güncellendi!")

if __name__ == "__main__":
    liste_olustur()
