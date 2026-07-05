# Alex Videoer

Ett-knapps Windows-app som laster ned nye videoer fra faste YouTube-kanaler
til en valgfri mappe (standard `~/Videos`, huskes i `mappe.txt`).
Design: `docs/superpowers/specs/2026-07-05-alex-videoer-design.md`.

## Bygge og levere

Hver push til `main` bygger `Alex Videoer.exe` og publiserer en GitHub-release
(v1, v2, ...). Førstegangslevering: last ned exe-fila fra Releases og lever
den via en minnepinne (FAT32/exFAT gir ingen mark-of-the-web, så SmartScreen
klager ikke). Legg den f.eks. på skrivebordet hos Alex.

## Oppdateringer

Appen ser etter ny release ved hver oppstart og bytter ut seg selv automatisk.
Push til `main` (eller kjør workflowen manuelt, f.eks. for å få med ny
yt-dlp når YouTube endrer seg) er alt som trengs; Alex får oppdateringen
neste gang han åpner appen.

## Endre kanaler

Rediger `channels.txt` i repoet, en kanal-URL per linje. Appen henter fila
fra GitHub ved hver kjøring (lokal kopi ved siden av exe-fila brukes som
reserve uten nett).

## Teste lokalt (macOS)

```sh
python3 -m venv .venv && .venv/bin/pip install "yt-dlp[default]" customtkinter
brew install deno python-tk
.venv/bin/python test_download.py   # selvtest
.venv/bin/python alex_videoer.py    # kjoer appen
```
