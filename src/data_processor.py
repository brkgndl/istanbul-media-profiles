# data_processor.py

import pandas as pd

# Mecra listesini tek bir sabit olarak tanımlıyoruz (tekrar etmemek için)
MECRALAR = [
    'Televizyon', 'Radyo', 'Gazete', 'İnternet sitesi haberleri',
    'Youtube kanalları', 'Sosyal Medya', 'Sosyal çevre', 'Aile', 'Diğer'
]
#Veriyi yükleyelim ve hazırlayalım
def veriyi_yukle_ve_hazirla(file_path):
    df = pd.read_excel(file_path)
    df = df.set_index('İlçe')
    df.columns = [col.strip() for col in df.columns]
    return df
#Sık kullanım oranlarını hesaplayalım 
def oranlari_hesapla(df):
    for mecra in MECRALAR:
        cols = [col for col in df.columns if col.startswith(mecra) and not col.endswith(('_Oran', '_Skoru'))]
        if len(cols) == 4:
            total = df[cols].sum(axis=1)
            total[total == 0] = 1
            df[f'{mecra}_Sık_Oran'] = df[cols[3]] / total
    df.fillna(0, inplace=True) #Eksik verileri 0 ile dolduralım ki oran hesaplamasında sorun olmasın
    return df
#Daha net yorumlayabilmek için kullanım yoğunluk skorunu da hesaplayalım
def kullanim_yogunluk_skoru(df):
    agirliklar_listesi = [0, 1, 2, 3] # Hiç, Nadiren, Ara sıra, Sıklıkla için ağırlık belirleyelim.

    for mecra in MECRALAR:
        cols = [col for col in df.columns if col.startswith(mecra) and not col.endswith(('_Oran', '_Skoru'))]
        if len(cols) == 4:
            agirlikli_toplam = df[cols].multiply(agirliklar_listesi, axis='columns').sum(axis=1)
            toplam_kisi = df[cols].sum(axis=1)
            toplam_kisi[toplam_kisi == 0] = 1 
            df[f'{mecra}_Kullanim_Yogunluk_Skoru'] = agirlikli_toplam / toplam_kisi
        else:
            print(f"Uyarı: '{mecra}' için 4 sütun bulunamadı, skor hesaplanmadı.")
    return df