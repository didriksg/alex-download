# Alex Videoer - design

A Windows app for a user with no technical experience: download new videos
from fixed YouTube channels with one button. All UI text is Norwegian.

## User experience

- Alex double-clicks `Alex Videoer.exe` (e.g. on the desktop).
- One window, one big button: **Hent nye videoer**, with a progress bar and
  a status line below.
- Two small buttons at the bottom: **Åpne videomappen** (opens the target
  folder in Explorer) and **Velg mappe** (folder picker; the choice is
  remembered).
- Done: "Ferdig! N nye videoer lagret."
- Errors (network down etc.): "Noe gikk galt, prøv igjen senere" plus the
  count that succeeded. Failed videos are not archived, so the next run
  retries them.

## Technical

- **Channels:** `channels.txt` in the repo, fetched from GitHub on every run;
  the local copy next to the exe is the offline fallback, and a baked-in
  default list (`https://www.youtube.com/@AlexSkoog-ks1pl`) is the last
  resort.
- **Target folder:** chosen with the native folder picker, stored in
  `folder.txt` next to the exe. Default: `~/Videos`. Videos land directly in
  the chosen folder (a USB stick can still be selected as the target).
- **Downloading:** yt-dlp as a Python library. `download_archive` lives in
  the target folder (`.downloaded.txt`) so "only new videos" works per
  target. Files: `<Channel>/<Title>.mp4`, capped at 1080p, MP4 (ffmpeg
  bundled for merging audio/video).
- **JS runtime:** yt-dlp now requires a JavaScript runtime for YouTube
  (`yt-dlp[default]` + Deno). Deno is bundled into the exe and wired up via
  `js_runtimes`.
- **UI:** CustomTkinter, dark theme: title, big rounded button, progress bar,
  status line, custom icon. Norwegian text.
- **Packaging:** PyInstaller `--onefile --windowed` on GitHub Actions
  (windows-latest); ffmpeg and deno are bundled. Every push to main publishes
  a GitHub release `v<run_number>` with the exe.
- **Auto-update:** at startup the app compares the newest release tag with
  its baked-in version number. If newer: download the exe, swap (the yt-dlp
  rename trick: a running exe can be renamed on Windows) and restart itself.
  Without network the check is skipped. Requires a public repo.

## Deliberately omitted

Installer, scheduled runs, quality settings, multi-user setup, code signing
(SmartScreen is avoided via USB-stick delivery), ffprobe (merging only needs
ffmpeg). Added only if reality demands it.
