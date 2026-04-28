import os

# İleride buraya istediğin kadar kanal ekleyebilirsin
m3u_icerik = """#EXTM3U
#EXTINF:-1,Kanal Test
http://test-yayin-linki.com/video.m3u8"""

# Listeyi GitHub'a kaydeden kısım
with open("yayin_listesi.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_icerik)

print("Liste başarıyla oluşturuldu!")
