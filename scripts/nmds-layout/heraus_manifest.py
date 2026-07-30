# Herausforderungen: Slug -> (cluster, seq, title). Erste Fassung — wird kuratiert.
# Ordnername = <seq>-<slug>; Cluster h1–h4 (siehe spaces.py / graph.ts).
_RAW = [
    ("selbstwert-leistung", "h1", 1, "Selbstwert an Leistung geknüpft"),
    ("perfektionismus", "h1", 2, "Perfektionismus & Fehlerangst"),
    ("eigene-reaktionen-bekaempfen", "h1", 3, "Das eigene Erleben bekämpfen"),
    ("selbstbestrafung", "h1", 4, "Schuld & Selbstbestrafung"),
    ("linearkausales-denken", "h1", 5, "Die Vergangenheit als Urteil"),
    ("problemtrance", "h1", 6, "Sich in die Problemtrance denken"),
    ("sozialer-vergleich", "h2", 7, "Der Vergleich nach oben"),
    ("einsamkeit", "h2", 8, "Einsamkeit trotz Vernetzung"),
    ("schwindende-verbundenheit", "h2", 9, "Schwindende gemeinsame Zeit"),
    ("partner-aendern-wollen", "h2", 10, "Den anderen zum Problem machen"),
    ("selbstaufgabe-beziehung", "h2", 11, "Selbstaufgabe in Beziehungen"),
    ("status-angst", "h2", 12, "Statusangst & Ungleichheit"),
    ("sinnkrise", "h3", 13, "Sinnverlust & verfeindete Werte"),
    ("steigende-erwartungen", "h3", 14, "Immer höhere Erwartungen"),
    ("ankunfts-trugschluss", "h3", 15, "Der Ankunfts-Trugschluss"),
    ("hedonische-anpassung", "h3", 16, "Die Glücks-Tretmühle"),
    ("ambivalenz-erzwingen", "h3", 17, "Eindeutigkeit erzwingen"),
    ("materialismus", "h3", 18, "Materialismus als Lebensziel"),
    ("zersplitterte-aufmerksamkeit", "h4", 19, "Zersplitterte Aufmerksamkeit"),
    ("fomo", "h4", 20, "Die Angst, etwas zu verpassen"),
    ("doomscrolling", "h4", 21, "Doomscrolling & Negativitätssog"),
    ("zeitarmut", "h4", 22, "Zeitarmut & Geschäftigkeitskult"),
    ("leistungsdruck-alwayson", "h4", 23, "Leistungsdruck ohne Aus"),
    ("naturentfremdung", "h4", 24, "Naturentfremdung"),
    ("zukunftsunsicherheit", "h4", 25, "Polykrise & Zukunftsangst"),
]
NODES = [{"slug": s, "cluster": c, "headings": [str(n)], "title": t} for (s, c, n, t) in _RAW]
BY_SLUG = {n["slug"]: n for n in NODES}
