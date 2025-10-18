# visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def gorselleri_olustur(df_processed, skor_son_eki, grafik_basligi):
    # İlgili sütunları dinamik olarak seçelim.
    skor_cols = [col for col in df_processed.columns if col.endswith(skor_son_eki)]
    df_skorlar = df_processed[skor_cols].copy()

   # Sütun isimlerini daha okunabilir hale getirelim
    etiketler = {
        col: col.replace(skor_son_eki, '')
                 .replace(' kanalları', '')
                 .replace(' Sitesi Haberleri', '')
                 .replace(' çevre', ' Çevre') 
        for col in skor_cols
    }
    df_plot = df_skorlar.rename(columns=etiketler)

    # Grafik 1: Korelasyon Matrisi 
    plt.figure(figsize=(12, 9))
    sns.heatmap(df_plot.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'{grafik_basligi} Arası Korelasyon', fontsize=16) 
    plt.show()

    # Grafik 2: Ortalama Skor Sütun Grafiği 
    plt.figure(figsize=(12, 7))
    ortalama_skorlar = df_plot.mean()
    ortalama_skorlar.sort_values(ascending=False).plot(kind='bar')
    plt.title(f'İstanbul Geneli {grafik_basligi} Ortalaması', fontsize=16) 
    plt.ylabel('Ortalama Skor')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # Grafik 3: İlçe Bazlı Skor Heatmap i
    plt.figure(figsize=(14, 10))
    sns.heatmap(df_plot, annot=True, cmap="YlGnBu") 
    plt.title(f"İlçe Bazında {grafik_basligi}", fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Dirsek Grafiği Çizme Fonksiyonu
def dirsek_grafigini_ciz(k_araligi, inertia_degerleri):
   
    plt.figure(figsize=(10, 6))
    plt.plot(k_araligi, inertia_degerleri, marker='o', linestyle='--')
    plt.xlabel('Küme Sayısı (k)')
    plt.ylabel('Inertia Değeri')
    plt.title('En Uygun Küme Sayısı için Dirsek Metodu')
    plt.xticks(k_araligi)
    plt.grid(True)
    plt.show()
# Radar Grafiği Çizme Fonksiyonu    
def radar_grafigini_ciz(kume_profilleri):
    
    # Etiketler ve açılar
    labels = [col.replace('_Kullanim_Yogunluk_Skoru', '').replace(' kanalları', '') for col in kume_profilleri.columns]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Küme 0 -> Mavi, Küme 1 -> Turuncu, Küme 2 -> Yeşil
    renkler = {
        0: '#1f77b4',  # Mavi
        1: '#ff7f0e',  # Turuncu
        2: '#2ca02c'   # Yeşil
    }

    # 2. Grafik Çizimi:
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Gelen DataFrame'deki her bir satırı (profili) çizelim.
    for i, row in kume_profilleri.iterrows():
        # 'i' burada kümenin numarasıdır (0, 1, veya 2).
        #Renk atamasını yapalım
        kume_rengi = renkler.get(i, '#808080')

        values = row.values.flatten().tolist()
        values += values[:1]
        
        ax.plot(angles, values, label=f'Küme {i}', linewidth=2, color=kume_rengi)
        ax.fill(angles, values, alpha=0.25, color=kume_rengi)

    # 3. Grafik Özelleştirmeleri:
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=11)
    plt.title('Medya Tüketim İmzası', size=18, y=1.1)
    
    # (legend) sadece birden fazla küme çiziliyorsa gösterelim.
    if len(kume_profilleri) > 1:
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # Streamlit için figürü döndürelim
    return fig