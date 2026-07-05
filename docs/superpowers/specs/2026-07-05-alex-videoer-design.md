# Alex Videoer - design

En Windows-app for en bruker uten teknisk erfaring: last ned nye videoer fra
faste YouTube-kanaler til en minnepinne, med en knapp.

## Brukeropplevelse

- Alex dobbeltklikker `Alex Videoer.exe` (ligger på minnepinnen).
- Ett vindu, en stor knapp: **Hent nye videoer**.
- Fremdrift vises som en tekstlinje ("Laster ned: <tittel> 43 %").
- Ferdig: "Ferdig! N nye videoer lagret. Du kan trygt ta ut minnepinnen."
- Ingen minnepinne: "Sett inn minnepinnen og prøv igjen."
- Feil (nett nede o.l.): "Noe gikk galt, prøv igjen senere" + antall som lyktes.
  Mislykkede videoer arkiveres ikke, så neste kjøring prøver dem igjen.

## Teknisk

- **Kanaler:** `channels.txt` ved siden av exe-fila, en URL per linje.
  Redigeres i Notisblokk, ingen ny bygging. Mangler fila brukes innebygd
  standardliste (kanalen `https://www.youtube.com/@AlexSkoog-ks1pl`).
- **Minnepinne:** Windows-API (GetDriveType == DRIVE_REMOVABLE). Nøyaktig én:
  brukes. Ingen: melding. Flere: enkel velger. macOS-fallback (/Volumes) kun
  for utvikling/test.
- **Nedlasting:** yt-dlp som Python-bibliotek. `download_archive` ligger PÅ
  pinnen (`Videoer/.downloaded.txt`) slik at "bare nye videoer" virker og
  pinnen er selvforsynt. Filer: `Videoer/<Kanal>/<Tittel>.mp4`, maks 1080p,
  MP4 (ffmpeg buntet for sammenslåing av lyd/bilde).
- **JS-runtime:** yt-dlp krever nå en JavaScript-runtime for YouTube
  (`yt-dlp[default]` + Deno). Deno buntes inn i exe-fila og pekes på via
  `js_runtimes`.
- **UI:** CustomTkinter, mørkt tema: tittel, stor rund knapp, fremdriftslinje,
  statuslinje, eget ikon. Norsk tekst.
- **Pakking:** PyInstaller `--onefile --windowed` på GitHub Actions
  (windows-latest); ffmpeg og deno buntes inn. Hver push til main publiserer
  en GitHub-release `v<run_number>` med exe-fila.
- **Auto-oppdatering:** ved oppstart sjekker appen nyeste release-tag mot
  innebygd versjonsnummer. Nyere: laster ned exe, bytter (rename-triksene til
  yt-dlp: kjørende exe kan omdøpes på Windows) og starter seg selv på nytt.
  Uten nett hoppes sjekken over. Krever offentlig repo.
- **Kanalliste:** hentes fra `channels.txt` i repoet (raw.githubusercontent)
  ved hver kjøring; lokal kopi ved siden av exe-fila som reserve, innebygd
  standardliste som siste utvei.
- **SmartScreen:** lever exe-fila via minnepinnen (FAT32/exFAT har ingen
  mark-of-the-web), så Alex aldri ser "Windows protected your PC".

## Bevisst utelatt

Installer, planlagte kjøringer, kvalitetsvalg, flerbrukeroppsett,
kodesignering (SmartScreen unngås via minnepinne-levering), ffprobe
(sammenslåing trenger bare ffmpeg). Legges til bare hvis virkeligheten
krever det.
