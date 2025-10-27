# main.py

from src.data_processor import veriyi_yukle_ve_hazirla, oranlari_hesapla, kullanim_yogunluk_skoru, ses_verisini_hazirla_ve_yukle
from src.visualizer import gorselleri_olustur, dirsek_grafigini_ciz, radar_grafigini_ciz, ses_kume_karsilastirma_ciz
from src.ml_processor import ilceleri_kumele, en_iyi_kume_sayisini_bul 
import os
import pandas as pd

# DOSYA YOLLARI
DOSYA_YOLU = 'data/raw/8-vdym-ilce-baznda-hanelerin-turkiye-gundemini-takip-ettii-mecralar-kullanm-skl.xlsx'
RAW_SES_DOSYA_YOLU = 'data/raw/2023-sosyoekonomi.xls'
PROCESSED_SES_DOSYA_YOLU = 'data/processed/istanbul_data_ses.xlsx' 

def main():
    # Medya verisini hazırlayalım
    temiz_df = veriyi_yukle_ve_hazirla(DOSYA_YOLU)
    islenmis_df = oranlari_hesapla(temiz_df.copy())
    islenmis_df = kullanim_yogunluk_skoru(islenmis_df)
    
    # SES verisini hazırlayalım
    ses_df = ses_verisini_hazirla_ve_yukle(RAW_SES_DOSYA_YOLU, PROCESSED_SES_DOSYA_YOLU)
    if ses_df is None:
        print("SES verisi yüklenemedi. Analizin SES karşılaştırması kısmı atlanacak.")

    #K means kümeleme
    
    # En iyi küme sayısını bul
    k_araligi, inertia_degerleri = en_iyi_kume_sayisini_bul(islenmis_df)
    
    if k_araligi:
        dirsek_grafigini_ciz(k_araligi, inertia_degerleri)

    EN_IYI_KUME_SAYISI = 3 
    print(f"\nGrafiğe göre en iyi küme sayısı {EN_IYI_KUME_SAYISI} olarak belirlendi. Analize devam ediliyor...")
    
    kumelenmis_df , siluet_skoru = ilceleri_kumele(islenmis_df, n_clusters=EN_IYI_KUME_SAYISI)
    
    # Kümeleme sonuçları (kumelenmis_df) ile SES verisini (ses_df) birleştir
    if ses_df is not None:
        birlesik_sonuc_df = kumelenmis_df.join(ses_df)
        
        kayip_sayisi = birlesik_sonuc_df["Ortalama SES skoru Average SES score"].isnull().sum()
        if kayip_sayisi > 0:
            print(f"UYARI: {kayip_sayisi} ilçe için SES skoru bulunamadı (İlçe isimleri uyuşmuyor olabilir).")
    else:
        print("SES verisi yüklenemedi. Karşılaştırma yapılamayacak.")
        birlesik_sonuc_df = kumelenmis_df.copy() 
    
    # GÖRSELLEŞTİRMELER

    #Radar grafiği (küme profilleri)
    if 'Kume' in birlesik_sonuc_df.columns:
        skor_sutunlari = birlesik_sonuc_df.filter(like='_Kullanim_Yogunluk_Skoru').columns
        kume_profilleri = birlesik_sonuc_df.groupby('Kume')[skor_sutunlari].mean()
        radar_grafigini_ciz(kume_profilleri)

    #Diğer görseller
    gorselleri_olustur(
        df_processed=birlesik_sonuc_df,
        skor_son_eki='_Sık_Oran', 
        grafik_basligi='Mecra Sık Kullanım Oranları'
    )
    
    gorselleri_olustur(
        df_processed=birlesik_sonuc_df, 
        skor_son_eki='_Kullanim_Yogunluk_Skoru', 
        grafik_basligi='Mecra Kullanım Yoğunluk Skorları'
    )
    
    # 3. SES Karşılaştırma Grafiği
    if ses_df is not None and 'Kume' in birlesik_sonuc_df.columns:
        ses_kume_karsilastirma_ciz(birlesik_sonuc_df)

    #Kaydetme
    
    output_dir = "data/processed" 
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "tum_ilce_sonuclari_ses_ve_kumeler.xlsx")
    birlesik_sonuc_df.to_excel(output_path, index=True)
    print(f"\nTüm skorları, küme ve SES bilgilerini içeren işlenmiş veri kaydedildi: {output_path}")

if __name__ == "__main__":
    main()