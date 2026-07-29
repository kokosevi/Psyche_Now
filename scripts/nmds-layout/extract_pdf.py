# scripts/nmds-layout/extract_pdf.py
"""Extrahiert die 2 Bischof-Kern-Bücher via pdftotext nach _extracted/ (gitignored).
Nur Textschicht (mit pdftotext verifiziert, kein OCR)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
MAT = os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie Materials")
OUT = os.path.join(MAT, "_extracted")

BOOKS = {
    "grundbuch": "Bischof Grundbuch.pdf",
    "theoretische-psychologie": "Bischof_2026_Theoretische-Psychologie.pdf",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for key, fname in BOOKS.items():
        src = os.path.join(MAT, fname)
        dst = os.path.join(OUT, f"{key}.txt")
        subprocess.run(["pdftotext", "-enc", "UTF-8", src, dst], check=True)
        n = len(open(dst, encoding="utf-8").read())
        print(f"{key}: {n} Zeichen -> {dst}")


if __name__ == "__main__":
    main()
