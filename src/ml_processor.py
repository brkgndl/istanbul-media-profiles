from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np  
import pandas as pd
# Kümeleme fonksiyonu
def ilceleri_kumele(df_islenmis, n_clusters=3):
    skor_sutunlari = df_islenmis.filter(like='_Kullanim_Yogunluk_Skoru').columns
    df_kumeleme = df_islenmis[skor_sutunlari]
    print(f"Analize dahil edilen {len(skor_sutunlari)} adet skor sütunu:")
    print(df_kumeleme.head())
# Veriyi standartlaştırma
    scaler = StandardScaler()
    veri_olceklenmis = scaler.fit_transform(df_kumeleme)
    print("\nVeri standartlaştırıldı.")

# KMeans ile kümeleme
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, random_state=42)
    kume_etiketleri = kmeans.fit_predict(veri_olceklenmis)
    print(f"\nİlçeler {n_clusters} kümeye ayrıldı.")
    score = silhouette_score(veri_olceklenmis, kume_etiketleri)
    print(f"\nModelin Siluet Skoru ({n_clusters} küme için): {score:.3f}")
    
    df_sonuc = df_islenmis.copy()
    df_sonuc['Kume'] = kume_etiketleri
    
    kume_profilleri = df_sonuc.groupby('Kume')[skor_sutunlari].mean()
    print("\nOluşturulan Kümelerin Profilleri (Ortalama Skorlar):")
    print(kume_profilleri)
    
    print("\nHer kümeye düşen ilçe sayısı:")
    print(df_sonuc['Kume'].value_counts())



    df_sonuc = df_islenmis.copy() 
    df_sonuc['Kume'] = kume_etiketleri
    kume_profilleri = df_sonuc.groupby('Kume')[skor_sutunlari].mean()
    
    print("\nOluşturulan Kümelerin Profilleri (Ortalama Skorlar):")
    print(kume_profilleri)
    print("\nHer kümeye düşen ilçe sayısı:")
    print(df_sonuc['Kume'].value_counts())
    print("Kümeler ve ilçelere göre dağılım:")
    for kume in range(n_clusters):
        ilceler = df_sonuc[df_sonuc['Kume'] == kume].index.tolist()
        print(f"Küme {kume}: {', '.join(ilceler)}")

    return df_sonuc , score
# Dirsek Metodu ile en iyi küme sayısını bulma fonksiyonu
def en_iyi_kume_sayisini_bul(df_islenmis):
    print("\nDirsek Metodu için inertia değerleri hesaplanıyor...")
    
    # Veriyi kümeleme için hazırlama
    skor_sutunlari = df_islenmis.filter(like='_Kullanim_Yogunluk_Skoru').columns
    df_kumeleme = df_islenmis[skor_sutunlari]

    if df_kumeleme.empty:
        print("Hata: Analiz için skor sütunları bulunamadı.")
        return None, None
# Veriyi standartlaştırma
    veri_olceklenmis = StandardScaler().fit_transform(df_kumeleme)
    
    # Farklı k değerleri için inertia ları saklayacağımız boş bir liste
    inertia_degerleri = []
    k_araligi = range(1, 11)  # 1'den 10'a kadar küme sayılarını deneyelim.
    for k in k_araligi:
        kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(veri_olceklenmis)
        inertia_degerleri.append(kmeans.inertia_)
        
    print("Inertia hesaplamaları tamamlandı.")
    return k_araligi, inertia_degerleri 