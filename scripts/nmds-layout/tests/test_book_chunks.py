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


SAMPLE_ARTIFACTS = """Echtes Kapitel Vorher.
1.1 Echtes Kapitel
Gültige Inhalte hier.
13.01.2014 14:59:54
Weitere Inhalte hier ohne Kapitelwechsel.
00 Grundkurs Psychologie (Bischof).indb 5
Immer noch Teil von 1.1.
30 Jahre die Lösung.
Immer noch Teil von 1.1.
1.2 Nächstes echtes Kapitel
Dieser Text gehört zu 1.2.
"""


def test_lehnt_timestamp_ab():
    """Reject PDF export timestamps like '13.01.2014 14:59:54'"""
    chs = {c["num"]: c for c in chapters(SAMPLE_ARTIFACTS)}
    assert "13.01.2014" not in chs
    # Timestamp sollte nicht im Text von 1.1 sein, aber der Text sollte die Inhalte NACH 1.1 enthalten
    if "1.1" in chs:
        assert "Weitere Inhalte" in chs["1.1"]["text"]


def test_lehnt_page_footer_ab():
    """Reject page footer lines like '00 Grundkurs... .indb 5'"""
    chs = {c["num"]: c for c in chapters(SAMPLE_ARTIFACTS)}
    assert "00" not in chs
    # .indb sollte nicht als Title erscheinen
    all_titles = [c["title"] for c in chs.values()]
    assert not any(".indb" in title for title in all_titles)


def test_lehnt_digit_sentence_ab():
    """Reject digit-led sentences ending with punctuation like '30 Jahre die Lösung.'"""
    chs = {c["num"]: c for c in chapters(SAMPLE_ARTIFACTS)}
    assert "30" not in chs
    # Aber 1.1 und 1.2 sollten da sein
    assert "1.1" in chs
    assert "1.2" in chs


if __name__ == "__main__":
    test_findet_nummerierte_kapitel()
    test_titel_und_text()
    test_ignoriert_unnummerierte_zeilen()
    test_lehnt_timestamp_ab()
    test_lehnt_page_footer_ab()
    test_lehnt_digit_sentence_ab()
    print("OK test_book_chunks")
