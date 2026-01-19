# Görev Yönetim Uygulaması (To-Do List) — Python (CLI + Gradio)

Bu repo, Python ile geliştirilmiş basit bir **Görev Yönetim Uygulaması (To-Do List)** içerir.  
Uygulama iki şekilde kullanılabilir:

- **CLI (Konsol Arayüzü)**: Talimatnameye uygun ana menü akışıyla görev ekleme/listeleme/düzenleme/silme.
- **Gradio (Web Arayüzü - Opsiyonel)**: Aynı görev listesini web arayüzünden yönetme + **dosya içeriğini canlı görme**.

## Özellikler

### Temel Özellikler (Talimatname)
- Ana menü: Listele / Ekle / Düzenle / Sil / Çıkış
- Görev ekleme (boş görev engeli)
- Görev listeleme (numaralı)
- Görev silme (numaraya göre, geçersiz giriş kontrolü)
- Görev düzenleme (numaraya göre, boş metin engeli)
- Görevleri **metin dosyasına** kaydetme ve açılışta okuma (utf-8)
- Hata durumlarını yönetme (dosya yok, okuma/yazma hataları, yanlış giriş)

### Ek Özellikler (İleri Seviye)
- Görev durum bilgisi: **tamamlandı / beklemede**
- Öncelik: **1 (yüksek) / 2 (orta) / 3 (düşük)**
- Son tarih: `YYYY-MM-DD` formatında isteğe bağlı alan
- Filtreleme: hepsi / bekleyen / tamamlanan
- Sıralama: yok / öncelik / son tarih
- Gradio'da kayıt dosyasını **canlı izleme** (Dosya sekmesi)

## Proje Yapısı

```text
todo-list/
├─ todo_core.py        # İş mantığı + dosya işlemleri
├─ todo_cli.py         # Konsol menü uygulaması
├─ todo_gradio.py      # (Opsiyonel) Gradio arayüzü
├─ requirements.txt    # Gradio için bağımlılıklar
└─ gorevler.txt        # Otomatik oluşur (kayıt dosyası)
