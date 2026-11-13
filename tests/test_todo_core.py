"""Regression tests for task dates and text-file compatibility."""

import tempfile
import unittest
from pathlib import Path

from todo_core import (
    gorev_ekle,
    gorevleri_kaydet,
    gorevleri_oku,
    gorunum_icin_liste,
)


class TodoCoreTests(unittest.TestCase):
    def test_date_is_normalized_when_adding(self):
        gorevler, mesaj = gorev_ekle([], "Rapor", son_tarih="2026-1-2")
        self.assertEqual(mesaj, "Görev eklendi.")
        self.assertEqual(gorevler[0].son_tarih, "2026-01-02")

    def test_sorting_uses_chronological_date_order(self):
        gorevler = []
        gorev_ekle(gorevler, "Daha geç", son_tarih="2026-01-10")
        gorev_ekle(gorevler, "Daha erken", son_tarih="2026-1-2")

        sirali = gorunum_icin_liste(gorevler, siralama="tarih")
        self.assertEqual([g.metin for g in sirali], ["Daha erken", "Daha geç"])

    def test_invalid_date_is_ignored(self):
        gorevler, _ = gorev_ekle([], "Test", son_tarih="2026-02-30")
        self.assertEqual(gorevler[0].son_tarih, "")

    def test_existing_records_are_normalized_on_read(self):
        with tempfile.TemporaryDirectory() as klasor:
            yol = Path(klasor) / "gorevler.txt"
            yol.write_text("0\t2\t2026-1-2\tRapor\n", encoding="utf-8")

            gorevler, hata = gorevleri_oku(str(yol))

        self.assertEqual(hata, "")
        self.assertEqual(gorevler[0].son_tarih, "2026-01-02")

    def test_legacy_plain_text_records_still_load(self):
        with tempfile.TemporaryDirectory() as klasor:
            yol = Path(klasor) / "gorevler.txt"
            yol.write_text("Eski görev\n", encoding="utf-8")

            gorevler, hata = gorevleri_oku(str(yol))

        self.assertEqual(hata, "")
        self.assertEqual(len(gorevler), 1)
        self.assertEqual(gorevler[0].metin, "Eski görev")
        self.assertEqual(gorevler[0].son_tarih, "")

    def test_normalized_dates_survive_save_and_reload(self):
        with tempfile.TemporaryDirectory() as klasor:
            yol = Path(klasor) / "gorevler.txt"
            gorevler, _ = gorev_ekle([], "Rapor", son_tarih="2026-1-2")
            self.assertEqual(gorevleri_kaydet(gorevler, str(yol)), "")

            tekrar, hata = gorevleri_oku(str(yol))

        self.assertEqual(hata, "")
        self.assertEqual(tekrar[0].son_tarih, "2026-01-02")


if __name__ == "__main__":
    unittest.main()
