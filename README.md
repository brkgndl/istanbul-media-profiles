# İstanbul Gündemi Nereden Takip Ediyor? 39 İlçenin Veri Bilimi ile 3 Ayrı Profili

Bu proje, İstanbul'un 39 ilçesinin medya tüketim alışkanlıklarını analiz eden ve ilçeleri 3 farklı medya profiline ayıran bir veri bilimi vaka çalışmasıdır. Proje, ham verinin işlenmesinden makine öğrenmesi modeline ve interaktif bir Streamlit uygulamasına kadar tüm adımları kapsamaktadır.

Projenin tüm hikayesi, metodolojisi ve derinlemesine yorumları **[Medium'da yayınlanacak vaka çalışmasında]** detaylıca anlatılacaktır.


## 🎯 Ana Bulgular: İstanbul'un 3 Medya Profili

Analizin ana sonucu, ilçelerin 3 net "medya tüketim imzasına" sahip olduğudur.


1.  **Geleneksel Medyanın Kalesi 📺:** TV'nin domine ettiği, ana akım odaklı profil.
2.  **Sakin Tüketiciler 🌿:** Tüm mecraları en düşük yoğunlukta tüketen, "seçici" profil.
3.  **Yüksek Erişimli Tüketiciler 🏙️:** Tüm kanalları (Dijital, Geleneksel, Sosyal) bir arada ve yüksek yoğunlukta kullanan "yüksek etkileşimli" profil.

---

## 🔬 Teknik Yaklaşım Özeti

Projenin metodolojik adımları şunlardır:

* **Özellik Mühendisliği:** 36+ ham sütundan ("Hiç", "Nadiren" vb.) `[0, 1, 2, 3]` ağırlıklandırması ile 9 adet **"Kullanım Yoğunluk Skoru"** metriği oluşturuldu.
* **Kümeleme:** İlçeler, bu skorlara göre **KMeans** algoritması ile gruplandırıldı.
* **Doğrulama:** En ideal küme sayısı (**3**) **Dirsek Metodu** ile bulundu ve kümelerin kalitesi **Siluet Skoru** (`0.399`) ile doğrulandı.

---

## 🛠️ Kullanılan Teknolojiler (Tech Stack)

* **Veri Analizi ve İşleme:** Python, Pandas, Numpy, openpyxl
* **Makine Öğrenmesi:** Scikit-learn (KMeans, StandardScaler, silhouette_score)
* **Görselleştirme:** Matplotlib, Seaborn
* **İnteraktif Uygulama:** Streamlit

## İletişim

Proje hakkında sorularınız veya geri bildirimleriniz için:

* **LinkedIn:** https://www.linkedin.com/in/sefa-burak-gündal/
* **E-Mail :** burakgundal1@icloud.com