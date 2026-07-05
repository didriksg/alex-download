# Alex Videoer

Ett-knapps Windows-app som laster ned nye videoer fra faste YouTube-kanaler
til en minnepinne. Design: `docs/superpowers/specs/2026-07-05-alex-videoer-design.md`.

## Bygge og levere

Hver push til `main` bygger `Alex Videoer.exe` og publiserer en GitHub-release
(v1, v2, ...). Førstegangslevering: last ned exe-fila fra Releases og legg den
på minnepinnen. Levert via minnepinne (FAT32/exFAT) får fila ingen
mark-of-the-web, så SmartScreen klager ikke. Exe-fila kan også kopieres til
skrivebordet for raskere oppstart (onefile pakker ut alt per start, tregt fra
gammel USB-pinne).

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
.venv/bin/python test_download.py                          # selvtest
ALEX_USB_DIR=/tmp/testusb .venv/bin/python alex_videoer.py # kjoer appen
```
