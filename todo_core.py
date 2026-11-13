# todo_core.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

VARSAYILAN_DOSYA = "gorevler.txt"


@dataclass
class Gorev:
    metin: str
    tamamlandi: bool = False
    oncelik: int = 2          # 1 (yüksek) - 3 (düşük)
    son_tarih: str = ""       # YYYY-MM-DD veya ""


def _temizle_metin(metin: str) -> str:
    metin = (metin or "").strip()
    metin = metin.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    while "  " in metin:
        metin = metin.replace("  ", " ")
    return metin


def _oncelik_duzelt(deger: int | str | None) -> int:
    try:
        x = int(deger)
    except (TypeError, ValueError):
        return 2
    return 1 if x < 1 else 3 if x > 3 else x


def _tarih_duzelt(tarih: str | None) -> str:
    t = (tarih or "").strip()
    if not t:
        return ""
    try:
        return datetime.strptime(t, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return ""


def gorevleri_oku(dosya_adi: str = VARSAYILAN_DOSYA) -> Tuple[List[Gorev], str]:
    try:
        with open(dosya_adi, "r", encoding="utf-8", errors="replace") as f:
            satirlar = f.read().splitlines()

        gorevler: List[Gorev] = []
        for s in satirlar:
            s = s.strip()
            if not s:
                continue

            # Yeni format: done \t priority \t due \t text
            parcalar = s.split("\t", 3)
            if len(parcalar) == 4:
                done_raw, pr_raw, due_raw, text_raw = parcalar
                done = str(done_raw).strip() == "1"
                pr = _oncelik_duzelt(pr_raw)
                due = _tarih_duzelt(due_raw)
                text = _temizle_metin(text_raw)
                if text:
                    gorevler.append(Gorev(text, done, pr, due))
            else:
                # Eski tek-satır görevleri de bozmadan içeri al
                text = _temizle_metin(s)
                if text:
                    gorevler.append(Gorev(text))

        return gorevler, ""
    except FileNotFoundError:
        return [], "Bilgi: Kayıt dosyası yok. Sıfırdan başlıyoruz."
    except OSError as e:
        return [], f"Hata: Dosya okunamadı ({e}). Sıfırdan başlıyoruz."


def gorevleri_kaydet(gorevler: List[Gorev], dosya_adi: str = VARSAYILAN_DOSYA) -> str:
    try:
        with open(dosya_adi, "w", encoding="utf-8", newline="\n") as f:
            for g in gorevler:
                done = "1" if g.tamamlandi else "0"
                pr = str(_oncelik_duzelt(g.oncelik))
                due = _tarih_duzelt(g.son_tarih)
                text = _temizle_metin(g.metin)
                if not text:
                    continue
                f.write(f"{done}\t{pr}\t{due}\t{text}\n")
        return ""
    except OSError as e:
        return f"Hata: Dosya kaydedilemedi ({e})."


def dosya_icerigi_oku(dosya_adi: str = VARSAYILAN_DOSYA) -> str:
    try:
        with open(dosya_adi, "r", encoding="utf-8", errors="replace") as f:
            icerik = f.read()
        return icerik if icerik.strip() else "(Dosya boş)"
    except FileNotFoundError:
        return "(Dosya henüz oluşmadı)"
    except OSError as e:
        return f"(Dosya okunamadı: {e})"


def gorev_listesi_metni(gorevler: List[Gorev]) -> str:
    if not gorevler:
        return "Görev listesi boş."

    satirlar = []
    for i, g in enumerate(gorevler, start=1):
        durum = "✓" if g.tamamlandi else " "
        pr = g.oncelik
        due = g.son_tarih if g.son_tarih else "-"
        satirlar.append(f"{i}) [{durum}] (Ö:{pr}) (T:{due})  {g.metin}")
    return "\n".join(satirlar)


def gorev_ekle(
    gorevler: List[Gorev],
    metin: str,
    oncelik: int | str | None = 2,
    son_tarih: str | None = "",
) -> Tuple[List[Gorev], str]:
    t = _temizle_metin(metin)
    if not t:
        return gorevler, "Hata: Boş görev eklenemez."

    gorevler.append(
        Gorev(
            metin=t,
            tamamlandi=False,
            oncelik=_oncelik_duzelt(oncelik),
            son_tarih=_tarih_duzelt(son_tarih),
        )
    )
    return gorevler, "Görev eklendi."


def gorev_sil(gorevler: List[Gorev], gorev_no_1den: int) -> Tuple[List[Gorev], str]:
    if not gorevler:
        return gorevler, "Hata: Liste boş; silinecek görev yok."

    if gorev_no_1den < 1 or gorev_no_1den > len(gorevler):
        return gorevler, "Hata: Geçersiz görev numarası."

    silinen = gorevler.pop(gorev_no_1den - 1)
    return gorevler, f"Görev silindi: {silinen.metin}"


def gorev_duzenle(
    gorevler: List[Gorev],
    gorev_no_1den: int,
    yeni_metin: str,
    yeni_oncelik: int | str | None = None,
    yeni_son_tarih: str | None = None,
    yeni_tamamlandi: Optional[bool] = None,
) -> Tuple[List[Gorev], str]:
    if not gorevler:
        return gorevler, "Hata: Liste boş; düzenlenecek görev yok."

    if gorev_no_1den < 1 or gorev_no_1den > len(gorevler):
        return gorevler, "Hata: Geçersiz görev numarası."

    t = _temizle_metin(yeni_metin)
    if not t:
        return gorevler, "Hata: Boş görev metni girilemez."

    g = gorevler[gorev_no_1den - 1]
    eski = g.metin

    g.metin = t
    if yeni_oncelik is not None and str(yeni_oncelik).strip() != "":
        g.oncelik = _oncelik_duzelt(yeni_oncelik)
    if yeni_son_tarih is not None:
        # boş bırakılırsa temizlemek için "" gönderilebilir
        g.son_tarih = _tarih_duzelt(yeni_son_tarih)
    if yeni_tamamlandi is not None:
        g.tamamlandi = bool(yeni_tamamlandi)

    return gorevler, f"Görev güncellendi: '{eski}' → '{g.metin}'"


def gorev_durum_degistir(gorevler: List[Gorev], gorev_no_1den: int) -> Tuple[List[Gorev], str]:
    if not gorevler:
        return gorevler, "Hata: Liste boş; değiştirilecek görev yok."

    if gorev_no_1den < 1 or gorev_no_1den > len(gorevler):
        return gorevler, "Hata: Geçersiz görev numarası."

    g = gorevler[gorev_no_1den - 1]
    g.tamamlandi = not g.tamamlandi
    durum = "tamamlandı" if g.tamamlandi else "beklemede"
    return gorevler, f"Durum güncellendi: {g.metin} ({durum})"


def gorunum_icin_liste(
    gorevler: List[Gorev],
    filtre: str = "hepsi",
    siralama: str = "yok",
) -> List[Gorev]:
    sonuc = gorevler[:]

    if filtre == "bekleyen":
        sonuc = [g for g in sonuc if not g.tamamlandi]
    elif filtre == "tamamlanan":
        sonuc = [g for g in sonuc if g.tamamlandi]

    if siralama == "oncelik":
        sonuc.sort(key=lambda g: (g.oncelik, g.son_tarih or "9999-12-31", g.metin.lower()))
    elif siralama == "tarih":
        sonuc.sort(key=lambda g: (g.son_tarih or "9999-12-31", g.oncelik, g.metin.lower()))

    return sonuc
