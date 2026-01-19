# todo_cli.py
from __future__ import annotations

from todo_core import (
    VARSAYILAN_DOSYA,
    gorevleri_oku,
    gorevleri_kaydet,
    gorev_listesi_metni,
    gorev_ekle,
    gorev_sil,
    gorev_duzenle,
    gorev_durum_degistir,
    gorunum_icin_liste,
)


def ana_menu() -> None:
    print("\n" + "═" * 44)
    print("  GÖREV YÖNETİMİ • To-Do (konsol sürümü)")
    print("═" * 44)
    print("1) Görevleri Listele")
    print("2) Yeni Görev Ekle")
    print("3) Görev Düzenle")
    print("4) Görev Sil")
    print("5) Çıkış")


def _sayi_al(etiket: str) -> int | None:
    try:
        return int(input(etiket).strip())
    except ValueError:
        return None


def _secim_al(etiket: str, izinli: set[str]) -> str:
    s = input(etiket).strip().lower()
    return s if s in izinli else ""


def _kaydet_ve_yaz(gorevler) -> None:
    msg = gorevleri_kaydet(gorevler, VARSAYILAN_DOSYA)
    if msg:
        print(msg)


def listeleme_ekrani(gorevler) -> None:
    if not gorevler:
        print("Görev listesi boş.")
        return

    print("\nListe görünümü:")
    print(" - (h) hepsi  (b) bekleyen  (t) tamamlanan")
    f = _secim_al("Filtre seç (enter=hepsi): ", {"h", "b", "t", ""})
    filtre = "hepsi" if f in {"h", ""} else "bekleyen" if f == "b" else "tamamlanan"

    print("Sıralama:")
    print(" - (y) yok  (o) öncelik  (s) son tarih")
    s = _secim_al("Sıralama seç (enter=yok): ", {"y", "o", "s", ""})
    siralama = "yok" if s in {"y", ""} else "oncelik" if s == "o" else "tarih"

    gorunum = gorunum_icin_liste(gorevler, filtre=filtre, siralama=siralama)
    print("\n--- GÖREVLER ---")
    print(gorev_listesi_metni(gorunum))


def main() -> None:
    gorevler, msg = gorevleri_oku(VARSAYILAN_DOSYA)
    if msg:
        print(msg)

    while True:
        ana_menu()
        secim = input("\nSeçiminiz (1-5): ").strip()

        if secim == "1":
            listeleme_ekrani(gorevler)

        elif secim == "2":
            metin = input("Görev: ")
            oncelik = input("Öncelik (1-3, enter=2): ").strip() or "2"
            son_tarih = input("Son tarih (YYYY-AA-GG, enter=boş): ").strip()

            gorevler, sonuc = gorev_ekle(gorevler, metin, oncelik, son_tarih)
            print(sonuc)
            if sonuc.startswith("Görev eklendi"):
                _kaydet_ve_yaz(gorevler)

        elif secim == "3":
            if not gorevler:
                print("Bilgi: Liste boş. Düzenlenecek görev yok.")
                continue

            print("\n--- GÖREVLER ---")
            print(gorev_listesi_metni(gorevler))

            no = _sayi_al("Düzenlenecek görev no: ")
            if no is None:
                print("Hata: Lütfen sayı girin.")
                continue

            yeni_metin = input("Yeni görev metni: ")

            print("Durum:")
            print(" - (d) değiştir  (t) tamamlandı  (b) beklemede  (enter=koru)")
            durum = _secim_al("Seçim: ", {"d", "t", "b", ""})
            yeni_tamam = None
            if durum == "t":
                yeni_tamam = True
            elif durum == "b":
                yeni_tamam = False

            yeni_oncelik = input("Yeni öncelik (1-3, enter=koru): ").strip()
            yeni_tarih = input("Yeni son tarih (YYYY-AA-GG, enter=koru, '-'=temizle): ").strip()

            if yeni_oncelik == "":
                yeni_oncelik_val = None
            else:
                yeni_oncelik_val = yeni_oncelik

            if yeni_tarih == "":
                yeni_tarih_val = None
            elif yeni_tarih == "-":
                yeni_tarih_val = ""
            else:
                yeni_tarih_val = yeni_tarih

            if durum == "d":
                gorevler, sonuc = gorev_durum_degistir(gorevler, no)
                print(sonuc)
                if sonuc.startswith("Durum güncellendi"):
                    _kaydet_ve_yaz(gorevler)

            gorevler, sonuc2 = gorev_duzenle(
                gorevler,
                no,
                yeni_metin,
                yeni_oncelik=yeni_oncelik_val,
                yeni_son_tarih=yeni_tarih_val,
                yeni_tamamlandi=yeni_tamam,
            )
            print(sonuc2)
            if sonuc2.startswith("Görev güncellendi"):
                _kaydet_ve_yaz(gorevler)

        elif secim == "4":
            if not gorevler:
                print("Bilgi: Liste boş. Silinecek görev yok.")
                continue

            print("\n--- GÖREVLER ---")
            print(gorev_listesi_metni(gorevler))

            no = _sayi_al("Silinecek görev no: ")
            if no is None:
                print("Hata: Lütfen sayı girin.")
                continue

            gorevler, sonuc = gorev_sil(gorevler, no)
            print(sonuc)
            if sonuc.startswith("Görev silindi"):
                _kaydet_ve_yaz(gorevler)

        elif secim == "5":
            _kaydet_ve_yaz(gorevler)
            print("Kapatıldı. Dosya güncel.")
            break

        else:
            print("Hata: Geçersiz seçim. 1-5 aralığını kullanın.")


if __name__ == "__main__":
    main()
