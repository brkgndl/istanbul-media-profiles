# app.py

import streamlit as st
import pandas as pd
from src.data_processor import veriyi_yukle_ve_hazirla, oranlari_hesapla, kullanim_yogunluk_skoru 
from src.ml_processor import ilceleri_kumele
from src.visualizer import radar_grafigini_ciz

# --- Sayfa Ayarları ---
st.set_page_config(page_title="İstanbul Medya Tüketim Analizi", layout="wide")
st.title("İstanbul'un Medya Tüketim Profilleri 📊")
st.write(" İstanbul'un 39 ilçesinin medya alışkanlıklarını inceleyen bu analiz, 3 ana tüketici profili ortaya çıkarıyor. Bu panelde, profillerin detaylarını ve hangi ilçelerin hangi gruba ait olduğunu interaktif olarak keşfedebilirsiniz.")

# --- Veri Yükleme ve İşleme
@st.cache_data # Veri işleme fonksiyonunu önbelleğe alır
def veri_akisini_calistir():
    DOSYA_YOLU = 'data/raw/8-vdym-ilce-baznda-hanelerin-turkiye-gundemini-takip-ettii-mecralar-kullanm-skl.xlsx'
    temiz_df = veriyi_yukle_ve_hazirla(DOSYA_YOLU)
    islenmis_df = oranlari_hesapla(temiz_df.copy())
    islenmis_df = kullanim_yogunluk_skoru(islenmis_df)

    kumelenmis_df , siluet_skoru = ilceleri_kumele(islenmis_df, n_clusters=3)

    return kumelenmis_df , siluet_skoru

kumelenmis_df , siluet_skoru = veri_akisini_calistir()

# İnteraktif Arayüz
st.header("Küme Profillerini İnceleyin")

# Küme profillerini hesapla
skor_sutunlari = kumelenmis_df.filter(like='_Kullanim_Yogunluk_Skoru').columns
kume_profilleri = kumelenmis_df.groupby('Kume')[skor_sutunlari].mean()

# İki sütunlu bir layout oluşturalım
col1, col2 = st.columns([1, 1.5]) 

with col1:
    st.subheader("Küme Detayları")

    # Küme profillerini adlandıralım
    kume_adlari = {
        0: "Geleneksel Medyanın Kalesi 📺",
        1: "Sakin Tüketiciler 🌿",
        2: "Yüksek Erişimli Tüketiciler  🏙️"
    }
    secilen_kume = st.radio("İncelemek istediğiniz profili seçin:", 
                            [0, 1, 2], 
                            format_func=lambda x: kume_adlari[x])

    st.markdown(f"### Seçilen Profil: **{kume_adlari[secilen_kume]}**")

    st.markdown("#### Bu Kümedeki İlçeler:")
    ilceler_list = kumelenmis_df[kumelenmis_df['Kume'] == secilen_kume].index.tolist()
    df_ilceler = pd.DataFrame(ilceler_list, columns=[" "]) 

    st.dataframe(
        df_ilceler, 
        height=300, 
        hide_index=True, # Sol taraftaki 0,1,2... satır numarasını gizler
        use_container_width=True # Tablonun sütuna tam sığmasını sağlar
    )

with col2:
    st.subheader("Medya Tüketim İmzası (Radar Grafiği)")
    # Seçilen kümenin profilini al
    tek_kume_profili = kume_profilleri[kume_profilleri.index == secilen_kume]

    # Radar grafiği fonksiyonunu çağıralım
    fig = radar_grafigini_ciz(tek_kume_profili) 
    st.pyplot(fig)

