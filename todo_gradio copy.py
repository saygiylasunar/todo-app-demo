# todo_gradio.py
from __future__ import annotations

import gradio as gr

from todo_core import (
    VARSAYILAN_DOSYA,
    dosya_icerigi_oku,
    gorevleri_oku,
    gorevleri_kaydet,
    gorev_listesi_metni,
    gorev_ekle,
    gorev_sil,
    gorev_duzenle,
    gorev_durum_degistir,
    gorunum_icin_liste,
)


def _dropdown_secimleri(gorevler):
    return [(f"{i}) {g.metin}", str(i)) for i, g in enumerate(gorevler, start=1)]


def yenile():
    gorevler, msg = gorevleri_oku(VARSAYILAN_DOSYA)
    liste = gorev_listesi_metni(gorevler)
    if msg:
        liste = msg + "\n\n" + liste
    return (
        gorevler,
        liste,
        gr.update(choices=_dropdown_secimleri(gorevler), value=None),
        dosya_icerigi_oku(VARSAYILAN_DOSYA),
    )


def gorunumu_guncelle(gorevler, filtre, siralama):
    gor = gorunum_icin_liste(gorevler, filtre=filtre, siralama=siralama)
    return gorev_listesi_metni(gor)


def ekle_islemi(gorevler, metin, oncelik, tarih):
    gorevler, msg = gorev_ekle(gorevler, metin, oncelik, tarih)
    if msg.startswith("Görev eklendi"):
        kayit = gorevleri_kaydet(gorevler, VARSAYILAN_DOSYA)
        if kayit:
            msg = msg + "\n" + kayit
    liste = msg + "\n\n" + gorev_listesi_metni(gorevler)
    return (
        gorevler,
        liste,
        gr.update(choices=_dropdown_secimleri(gorevler), value=None),
        "",
        dosya_icerigi_oku(VARSAYILAN_DOSYA),
    )


def sil_islemi(gorevler, secilen_no):
    if not secilen_no:
        liste = "Hata: Silmek için bir görev seçmelisiniz.\n\n" + gorev_listesi_metni(gorevler)
        return gorevler, liste, gr.update(choices=_dropdown_secimleri(gorevler), value=None), dosya_icerigi_oku(VARSAYILAN_DOSYA)

    gorevler, msg = gorev_sil(gorevler, int(secilen_no))
    if msg.startswith("Görev silindi"):
        kayit = gorevleri_kaydet(gorevler, VARSAYILAN_DOSYA)
        if kayit:
            msg = msg + "\n" + kayit
    liste = msg + "\n\n" + gorev_listesi_metni(gorevler)
    return gorevler, liste, gr.update(choices=_dropdown_secimleri(gorevler), value=None), dosya_icerigi_oku(VARSAYILAN_DOSYA)


def durum_degistir_islemi(gorevler, secilen_no):
    if not secilen_no:
        liste = "Hata: Durum değiştirmek için bir görev seçmelisiniz.\n\n" + gorev_listesi_metni(gorevler)
        return gorevler, liste, gr.update(choices=_dropdown_secimleri(gorevler), value=None), dosya_icerigi_oku(VARSAYILAN_DOSYA)

    gorevler, msg = gorev_durum_degistir(gorevler, int(secilen_no))
    if msg.startswith("Durum güncellendi"):
        kayit = gorevleri_kaydet(gorevler, VARSAYILAN_DOSYA)
        if kayit:
            msg = msg + "\n" + kayit
    liste = msg + "\n\n" + gorev_listesi_metni(gorevler)
    return gorevler, liste, gr.update(choices=_dropdown_secimleri(gorevler), value=None), dosya_icerigi_oku(VARSAYILAN_DOSYA)


def duzenle_islemi(gorevler, secilen_no, yeni_metin, yeni_oncelik, yeni_tarih, tamamlandi_sec):
    if not secilen_no:
        liste = "Hata: Düzenlemek için bir görev seçmelisiniz.\n\n" + gorev_listesi_metni(gorevler)
        return gorevler, liste, gr.update(choices=_dropdown_secimleri(gorevler), value=None), "", dosya_icerigi_oku(VARSAYILAN_DOSYA)

    if yeni_tarih.strip() == "-":
        yeni_tarih = ""

    gorevler, msg = gorev_duzenle(
        gorevler,
        int(secilen_no),
        yeni_metin,
        yeni_oncelik=yeni_oncelik if str(yeni_oncelik).strip() != "" else None,
        yeni_son_tarih=yeni_tarih,
        yeni_tamamlandi=bool(tamamlandi_sec),
    )
    if msg.startswith("Görev güncellendi"):
        kayit = gorevleri_kaydet(gorevler, VARSAYILAN_DOSYA)
        if kayit:
            msg = msg + "\n" + kayit

    liste = msg + "\n\n" + gorev_listesi_metni(gorevler)
    return (
        gorevler,
        liste,
        gr.update(choices=_dropdown_secimleri(gorevler), value=None),
        "",
        dosya_icerigi_oku(VARSAYILAN_DOSYA),
    )


with gr.Blocks(title="To-Do • Görev Yönetimi") as demo:
    gr.Markdown("## Görev Yönetimi (To-Do)\nKonsol projesinin üstüne eklenmiş hafif bir arayüz katmanı.")

    gorev_state = gr.State([])

    with gr.Tabs():
        with gr.TabItem("Görevler"):
            durum_liste = gr.Textbox(label="Liste / Durum", lines=12)

            with gr.Accordion("Görünüm Ayarları", open=False):
                with gr.Row():
                    filtre = gr.Dropdown(
                        label="Filtre",
                        choices=[("Hepsi", "hepsi"), ("Bekleyen", "bekleyen"), ("Tamamlanan", "tamamlanan")],
                        value="hepsi",
                    )
                    siralama = gr.Dropdown(
                        label="Sıralama",
                        choices=[("Yok", "yok"), ("Öncelik", "oncelik"), ("Son Tarih", "tarih")],
                        value="yok",
                    )
                gorunum_btn = gr.Button("Görünümü Uygula")

            gr.Markdown("### Yeni Görev")
            with gr.Row():
                yeni_metin = gr.Textbox(label="Görev metni", placeholder="Örn: Sunum slaytlarını toparla", scale=4)
                yeni_oncelik = gr.Dropdown(label="Öncelik", choices=["1", "2", "3"], value="2", scale=1)
                yeni_tarih = gr.Textbox(label="Son tarih", placeholder="YYYY-MM-DD (boş bırakılabilir)", scale=2)
                ekle_btn = gr.Button("Ekle", scale=1)

            gr.Markdown("### Düzenle / Sil / Durum")
            with gr.Row():
                secim = gr.Dropdown(label="Görev seç", choices=[], value=None, scale=2)
                duzen_metin = gr.Textbox(label="Yeni metin", placeholder="Seçilen görevi güncelle", scale=3)

            with gr.Row():
                duzen_oncelik = gr.Dropdown(label="Yeni öncelik", choices=["1", "2", "3"], value="2")
                duzen_tarih = gr.Textbox(label="Yeni son tarih", placeholder="YYYY-MM-DD | '-' yazarsan temizler", value="")
                duzen_tamam = gr.Checkbox(label="Tamamlandı", value=False)

            with gr.Row():
                duzenle_btn = gr.Button("Düzenle")
                durum_btn = gr.Button("Durum Değiştir (toggle)")
                sil_btn = gr.Button("Sil")
                yenile_btn = gr.Button("Yenile")

        with gr.TabItem("Dosya (canlı)"):
            gr.Markdown("### Kayıt dosyasının anlık içeriği")
            dosya_kutu = gr.Code(label=f"{VARSAYILAN_DOSYA}", language="text")
            yenile2_btn = gr.Button("Dosyayı Yenile")

    demo.load(fn=yenile, inputs=[], outputs=[gorev_state, durum_liste, secim, dosya_kutu])

    yenile_btn.click(fn=yenile, inputs=[], outputs=[gorev_state, durum_liste, secim, dosya_kutu])
    yenile2_btn.click(fn=yenile, inputs=[], outputs=[gorev_state, durum_liste, secim, dosya_kutu])

    gorunum_btn.click(fn=gorunumu_guncelle, inputs=[gorev_state, filtre, siralama], outputs=[durum_liste])

    ekle_btn.click(
        fn=ekle_islemi,
        inputs=[gorev_state, yeni_metin, yeni_oncelik, yeni_tarih],
        outputs=[gorev_state, durum_liste, secim, yeni_metin, dosya_kutu],
    )

    sil_btn.click(
        fn=sil_islemi,
        inputs=[gorev_state, secim],
        outputs=[gorev_state, durum_liste, secim, dosya_kutu],
    )

    durum_btn.click(
        fn=durum_degistir_islemi,
        inputs=[gorev_state, secim],
        outputs=[gorev_state, durum_liste, secim, dosya_kutu],
    )

    duzenle_btn.click(
        fn=duzenle_islemi,
        inputs=[gorev_state, secim, duzen_metin, duzen_oncelik, duzen_tarih, duzen_tamam],
        outputs=[gorev_state, durum_liste, secim, duzen_metin, dosya_kutu],
    )


if __name__ == "__main__":
    demo.launch()
