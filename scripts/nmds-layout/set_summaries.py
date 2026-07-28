import re, os

THEMEN = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..",
                                        "site", "src", "content", "themen"))

S = {
    "sag-mal-gunther": "Ein persönliches Porträt von Gunther Schmidt — welche Werthaltungen, Prägungen und Momente seine Neugier für die Vielfalt menschlichen Erlebens geweckt haben.",
    "werdegang-wurzeln": "Gunther Schmidts Weg von der Volkswirtschaft über die Medizin zur Familien- und Hypnotherapie — die Wurzeln des hypnosystemischen Ansatzes.",
    "hypnosyst-denken": "Kontextbezug statt fester Bedeutung: Jedes Phänomen wird erst im Wechselwirkungskontext verständlich — kein Erleben wirkt aus sich heraus.",
    "rollenverstaendnis": "Therapie als achtungsvolle Kooperation, in der Klient:innen erleben, dass ihre Potenziale vorhanden sind und aktiviert werden können.",
    "haltung": "Menschen sind nie festgelegt, sondern tragen tausende Erlebnismöglichkeiten in sich — von tiefster Verzweiflung bis kraftvoller Handlungsfähigkeit.",
    "zuweisungsdynamik": "Der erste Schritt jedes Prozesses: klären, wie und von wem die Idee zur Beratung entstand — und in welchem Kontext.",
    "utilisation-problemsituationen": "Belastende Situationen werden gewürdigt und rekontextualisiert statt bekämpft — auch der berichtete Druck wird nutzbar gemacht.",
    "utilisation-ambivalenzen": "Hinter blockierten Kompetenzen stecken oft unbewusste gute Gründe: verborgene Zielkonflikte werden aufgedeckt und gewürdigt.",
    "utilisation-rueckfaelle": "Rückfälle als Ehrenrunden verstehen — der schädigende Begriff wird ersetzt, das Wiederauftauchen alter Muster nutzbar gemacht.",
    "abschluss-transfer": "Transfer ist keine Schlussphase, sondern Aufgabe jeder Sitzung — gegen die tausendfachen Alltags-Einladungen in die alte Richtung.",
    "fallanalyse-ungewisses": "Eine ausführliche Fallanalyse (Unternehmerin in existenzieller Stresskrise) zeigt die hypnosystemischen Prinzipien im Umgang mit dem Ungewissen.",
    "imagination-steuerposition": "Eine Imaginationsübung, die einen geschützten Beobachterplatz aufbaut — eine Steuerposition, die vor belastenden Narrativen schützt.",
    "depression": "Depression nicht als statische Diagnose, sondern als unwillkürlich selbsterzeugter Prozess — mit den entsprechenden therapeutischen Ansatzpunkten.",
    "trauer-schuld": "Trauer und Schuld als dynamische, selbsterzeugte Prozesse mit wichtiger Funktion — und wie sich damit hypnosystemisch arbeiten lässt.",
    "schmerzen": "Chronische Schmerzen im Licht von Hirnforschung und Gate-Control-Theorie — unwillkürliche Prozesse und die daraus folgenden Interventionsprinzipien.",
    "panik": "Angst und Panik als autopoietisch selbsterzeugte, meist unbewusste Prozesse — mit spezifischen Strukturen und Interventionsmöglichkeiten.",
    "paarkonflikt": "Hypnosystemische Paararbeit: systemische Wechselwirkungen, Auftragsgestaltung und bezogene Individuation in typischen Paardynamiken.",
    "trauma": "Trauma wirkt nicht, weil es geschah, sondern weil es heute wieder ins Zentrum rückt — ein Verständnis jenseits linear-kausaler Ursache-Wirkung.",
    "sucht": "Sucht als Suchkompetenz statt Pathologie: hinter jeder Sucht steht eine Sehnsucht nach ersehntem Erleben — und ein Lösungsversuch.",
    "essverhalten": "Ess- und Bewegungsthemen hypnosystemisch: Aufklärung über Hypnose-Missverständnisse und der Umgang mit der besonderen Gewichtsthematik.",
}


def main():
    for slug, summ in S.items():
        assert '"' not in summ, ("straight quote in", slug)
        p = os.path.join(THEMEN, slug + ".md")
        t = open(p, encoding="utf-8").read()
        t2, n = re.subn(r'^summary: ".*?"$', f'summary: "{summ}"', t, count=1, flags=re.M)
        assert n == 1, ("summary line not found:", slug)
        open(p, "w", encoding="utf-8").write(t2)
    print("Summaries gesetzt:", len(S))


if __name__ == "__main__":
    main()
