# main.py

from data_processor import veriyi_yukle_ve_hazirla, oranlari_hesapla, kullanim_yogunluk_skoru
from visualizer import gorselleri_olustur, dirsek_grafigini_ciz, radar_grafigini_ciz
from ml_processor import ilceleri_kumele, en_iyi_kume_sayisini_bul 
import os

# DOSYA YOLU 
DOSYA_YOLU = 'data/raw/8-vdym-ilce-baznda-hanelerin-turkiye-gundemini-takip-ettii-mecralar-kullanm-skl.xlsx'

def main():
    # Veriyi hazırlayalım ve skorları üretelim
    temiz_df = veriyi_yukle_ve_hazirla(DOSYA_YOLU)
    islenmis_df = oranlari_hesapla(temiz_df.copy())
    islenmis_df = kullanim_yogunluk_skoru(islenmis_df)

    k_araligi, inertia_degerleri = en_iyi_kume_sayisini_bul(islenmis_df)
    
    # Eğer hesaplama başarılıysa grafiği çizdirelim.
    if k_araligi:
        dirsek_grafigini_ciz(k_araligi, inertia_degerleri)

    # Grafiğe göre en iyi küme sayısını belirleyip analize devam edelim.
    # Grafikteki dirsek noktasını belirleyip değişkene atayalım.
    EN_IYI_KUME_SAYISI = 3 

    print(f"\nGrafiğe göre en iyi küme sayısı {EN_IYI_KUME_SAYISI} olarak belirlendi. Analize devam ediliyor...")
    kumelenmis_df , siluet_skoru = ilceleri_kumele(islenmis_df, n_clusters=EN_IYI_KUME_SAYISI)
    
    # Kümeleme fonksiyonu
    # Skorları ürettikten sonra, bu skorları kullanarak ilçeleri kümeliyoruz.

    if 'Kume' in kumelenmis_df.columns:
        
        # Küme profillerini (her kümenin ortalama skorlarını) hesaplayalım
        skor_sutunlari = kumelenmis_df.filter(like='_Kullanim_Yogunluk_Skoru').columns
        kume_profilleri = kumelenmis_df.groupby('Kume')[skor_sutunlari].mean()
        
        # Fonksiyonumuzu bu profillerle çağıralım
        radar_grafigini_ciz(kume_profilleri)


    gorselleri_olustur(
        df_processed=kumelenmis_df, 
        skor_son_eki='_Sık_Oran', 
        grafik_basligi='Mecra Sık Kullanım Oranları'
    )
    
    gorselleri_olustur(
        df_processed=kumelenmis_df, 
        skor_son_eki='_Kullanim_Yogunluk_Skoru', 
        grafik_basligi='Mecra Kullanım Yoğunluk Skorları'
    )

    # İşlenmiş ve kümelenmiş veriyi kaydedelim.
    output_dir = "data/processed" 
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "ilce_bazli_skorlar_ve_kumeler.xlsx")
    kumelenmis_df.to_excel(output_path, index=True)
    print(f"\nTüm skorları ve küme bilgilerini içeren işlenmiş veri kaydedildi: {output_path}")

if __name__ == "__main__":
    main()