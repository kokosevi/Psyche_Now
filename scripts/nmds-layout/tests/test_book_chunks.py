import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from book_chunks import chapters

SAMPLE = """Vorwort ohne Nummer, wird ignoriert.
1 Einstimmung
Erster Rumpf.
1.1 Das öffentliche Geheimnis
Zweiter Rumpf über Wahrnehmung.
1.1.1 Warten auf den Knoten
Dritter Rumpf über Motivation und Sollwert.
2 Nächstes Kapitel
Vierter Rumpf.
"""


def test_findet_nummerierte_kapitel():
    chs = chapters(SAMPLE)
    nums = [c["num"] for c in chs]
    assert nums == ["1", "1.1", "1.1.1", "2"], nums


def test_titel_und_text():
    chs = {c["num"]: c for c in chapters(SAMPLE)}
    assert chs["1.1"]["title"] == "Das öffentliche Geheimnis"
    assert "Wahrnehmung" in chs["1.1"]["text"]
    # Text endet vor der nächsten Überschrift
    assert "Motivation" not in chs["1.1"]["text"]


def test_ignoriert_unnummerierte_zeilen():
    chs = chapters(SAMPLE)
    assert all(c["title"] for c in chs)
    assert "Vorwort" not in " ".join(c["num"] for c in chs)


if __name__ == "__main__":
    test_findet_nummerierte_kapitel()
    test_titel_und_text()
    test_ignoriert_unnummerierte_zeilen()
    print("OK test_book_chunks")
