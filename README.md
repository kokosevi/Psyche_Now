# Psyche_Now

Eine interaktive Homepage rund um Psychologie (u. a. Allgemeine Psychologie,
Hypnosystemik) mit Selbsttests, interaktiven Diagrammen, Scroll-Storytelling,
durchsuchbaren Inhalten und einer Wissens-**Graph-Ansicht**.

- **Kein** Login, **keine** Zahlung, **keine** Datenbank — alle Inhalte leben als
  Markdown im Repo.
- Gebaut mit **Astro**, gehostet auf **Netlify**, Statistik über **Umami**.

## Workflow

Der komplette Ablauf (Design → Code → GitHub → Netlify → Umami) und die Antwort auf
"Wann arbeite ich in Claude Design, wann in Claude Code?" steht in
**[docs/WORKFLOW.md](docs/WORKFLOW.md)**.

## Ordner

| Ordner        | Inhalt                                                        |
|---------------|--------------------------------------------------------------|
| `site/`       | Das Astro-Projekt (Homepage-Code) — wird beim Scaffold angelegt |
| `content/`    | Roh-Notizen & Entwürfe                                       |
| `Bibliothek/` | Inhaltliche Quellen (PDFs, Slides) — Kontext, kein Website-Text |
| `design/`     | Hand-off aus Claude Design (Artifacts, Screenshots, HANDOFF.md) |
| `reference/`  | Design-Tokens & Referenzen                                   |
| `docs/`       | Workflow-Dokumentation                                       |

## Lokale Entwicklung (sobald `site/` existiert)

```bash
cd site
npm install
npm run dev
```
