# data_processor.py

import pandas as pd
import os

# Mecra listesini tek bir sabit olarak tanımlıyoruz (tekrar etmemek için)
MECRALAR = [
    'Televizyon', 'Radyo', 'Gazete', 'İnternet sitesi haberleri',
    'Youtube kanalları', 'Sosyal Medya', 'Sosyal çevre', 'Aile', 'Diğer'
]
#Veriyi yükleyelim ve hazırlayalım
def veriyi_yukle_ve_hazirla(file_path):
    df = pd.read_excel(file_path)
    df = df.set_index('İlçe')
    df.index = (df.index.str.strip()
                          .str.replace('İ', 'I')
                          .str.replace('Ş', 'S')
                          .str.replace('Ğ', 'G')
                          .str.replace('Ü', 'U')
                          .str.replace('Ö', 'O')
                          .str.replace('Ç', 'C'))
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

def ses_verisini_hazirla_ve_yukle(raw_file_path, processed_file_path):
   #İşlenmiş SES dosyasını elde etme 
    try:
        #Eğer işlenmiş dosya varsa yükleme
        df_ses = pd.read_excel(processed_file_path, index_col=0)
        
        #İndeksi gerekli şekilde normalize edelim
        df_ses.index = (df_ses.index.str.upper().str.strip()
                                  .str.replace('İ', 'I')
                                  .str.replace('Ş', 'S')
                                  .str.replace('Ğ', 'G')
                                  .str.replace('Ü', 'U')
                                  .str.replace('Ö', 'O')
                                  .str.replace('Ç', 'C'))
        
        return df_ses

    except FileNotFoundError:
        #Dosya bulunamadıysa raw veriden oluşturma
        print(f"Ham veriden ({raw_file_path}) oluşturuluyor...")
        
        try:
            df = pd.read_excel(raw_file_path, skiprows=4)
            df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()
            df_istanbul = df[df["İl Province"] == 'İstanbul'].copy()
            
            if df_istanbul.empty:
                print("HATA: 'İstanbul' ili ham veride bulunamadı.")
                return None

            df_istanbul.set_index("İlçe District", inplace=True)
            ses_kolonu = "Ortalama SES skoru Average SES score"
            
            if ses_kolonu not in df_istanbul.columns:
                print(f"HATA: '{ses_kolonu}' sütunu ham veride bulunamadı.")
                return None
                
            df_ses = df_istanbul[[ses_kolonu]]
            
            df_ses.index = (df_ses.index.str.upper().str.strip()
                                      .str.replace('İ', 'I')
                                      .str.replace('Ş', 'S')
                                      .str.replace('Ğ', 'G')
                                      .str.replace('Ü', 'U')
                                      .str.replace('Ö', 'O')
                                      .str.replace('Ç', 'C'))
            
            #Çıktı
            output_dir = os.path.dirname(processed_file_path)
            os.makedirs(output_dir, exist_ok=True)
            
            # İstenen dosyayı kaydedelim
            df_ses.to_excel(processed_file_path, index=True)
            print(f"Başarılı: Yeni SES verisi şuraya kaydedildi: {processed_file_path}")
            
            return df_ses
            
        except FileNotFoundError:
            print(f"HATA: Ham SES dosyası bulunamadı: {raw_file_path}")
            return None
        except Exception as e:
            print(f"Ham SES verisi işlenirken bir hata oluştu: {e}")
            return None
            
    except Exception as e:
        print(f"İşlenmiş SES verisi okunurken bir hata oluştu: {e}")
        return None