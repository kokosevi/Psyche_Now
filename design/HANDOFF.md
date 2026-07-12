# Hand-off: Claude Design → Claude Code

Diese Datei ist die Brücke zwischen dem visuellen Entwurf (claude.ai) und dem
echten Code (Claude Code). Für **jeden** Screen / jede Komponente, die du aus
Claude Design übergibst, füllst du unten einen Block aus dem Template aus.

## So läuft ein Hand-off ab

1. In Claude Design den Screen als **Artifact** (HTML/React) fertigstellen.
2. Artifact-Code speichern → `design/artifacts/<screen-name>/`
3. Screenshot speichern → `design/screenshots/<screen-name>.png`
4. Unten einen neuen Block aus dem **Template** ausfüllen.
5. In Claude Code sagen: *"Bitte Hand-off `<screen-name>` umsetzen."*

> Tipp: Halte dich beim Design an `reference/design-tokens.md` und benenne
> Farben/Schriften beim Namen. Dann sieht der gebaute Code aus wie dein Mockup.

---

## Template (kopieren pro Screen)

```markdown
### <screen-name>            <!-- z. B. "startseite-hero" -->

- **Status:** 🟡 offen | 🟢 umgesetzt
- **Datum:**  YYYY-MM-DD
- **Artifact-Code:** design/artifacts/<screen-name>/
- **Screenshot:**    design/screenshots/<screen-name>.png

**Was ist das?**
Ein Satz: welcher Screen / welche Komponente.

**Wohin gehört es?**
Welche Seite / welcher Bereich der Homepage (z. B. Startseite, Themen-Seite, Graph-Ansicht).

**Interaktives Verhalten**
Was soll passieren (Klick, Hover, Scroll, Eingabe)? Was ist bewusst statisch?

**Inhalt**
Woher kommt der echte Text/Daten? (z. B. `site/src/content/themen/…`, oder "Platzhalter,
kommt später"). Was im Mockup ist echt, was ist Dummy?

**Abweichungen / Hinweise**
Alles, was im Code anders sein soll als im Mockup, oder worauf ich achten soll.
```

---

## Hand-offs

<!-- Neueste zuerst. Ersten echten Eintrag hier unter dieser Zeile einfügen. -->

### beispiel-startseite-hero   (Beispiel — beim ersten echten Hand-off ersetzen)

- **Status:** 🟡 offen
- **Datum:**  2026-07-12
- **Artifact-Code:** design/artifacts/beispiel-startseite-hero/
- **Screenshot:**    design/screenshots/beispiel-startseite-hero.png

**Was ist das?**
Der obere Bereich der Startseite mit Titel, Untertitel und einem Button zur Graph-Ansicht.

**Wohin gehört es?**
Startseite, ganz oben (Hero-Bereich).

**Interaktives Verhalten**
Button "Themen erkunden" führt zur Graph-Ansicht. Sanftes Einblenden beim Laden.
Rest ist statisch.

**Inhalt**
Titel und Untertitel sind echt (siehe Screenshot). Der Button-Link zeigt vorerst auf
`/graph` (Platzhalter, Seite kommt später).

**Abweichungen / Hinweise**
Nur ein Beispiel, um das Format zu zeigen — beim ersten echten Design ersetzen.
