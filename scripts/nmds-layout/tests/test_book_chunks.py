import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from book_chunks import passages, _clean_lines

SAMPLE = """13.01.2014 14:59:54
Erster Absatz über Wahrnehmung und Farbe.
00 Grundkurs Psychologie (Bischof).indb 5

Zweiter Absatz über Motivation und Sollwert.

123
Dritter Absatz über Regelkreise.
"""


def test_entfernt_seiten_moeblierung():
    joined = "\n".join(_clean_lines(SAMPLE))
    assert "13.01.2014" not in joined          # Export-Timestamp weg
    assert ".indb" not in joined               # Footer weg
    assert "\n123\n" not in "\n" + joined + "\n"  # reine Seitenzahl weg
    assert "Wahrnehmung" in joined             # echter Text bleibt


def test_fenstert_nach_wortzahl():
    text = "\n\n".join(f"Absatz {i} " + "wort " * 60 for i in range(5))
    chs = passages(text, target_words=100)
    assert len(chs) >= 2                        # 5×~61 Wörter -> mehrere Fenster
    assert all(c["text"].strip() for c in chs)


def test_kurzer_text_ein_chunk():
    chs = passages("Nur ein kurzer Absatz.", target_words=200)
    assert len(chs) == 1 and "kurzer" in chs[0]["text"]


def test_fenster_ueberschreitet_ziel_nicht_grob():
    # ein sehr langer Absatz (1000 Wörter) muss in mehrere Fenster zerfallen
    text = "kopf\n\n" + "wort " * 1000
    chs = passages(text, target_words=200)
    assert max(len(c["text"].split()) for c in chs) <= 400   # ≤ 2× Ziel
    assert len(chs) >= 4


if __name__ == "__main__":
    test_entfernt_seiten_moeblierung()
    test_fenstert_nach_wortzahl()
    test_kurzer_text_ein_chunk()
    test_fenster_ueberschreitet_ziel_nicht_grob()
    print("OK test_book_chunks")
