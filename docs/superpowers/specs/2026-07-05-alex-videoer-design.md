# Alex Videoer - design

A Windows app for a user with no technical experience: download new videos
from fixed YouTube channels with one button. All UI text is Norwegian.

## User experience

- Alex double-clicks `Alex Videoer.exe` (e.g. on the desktop).
- The window title and header show the first channel's display name (fetched
  at startup; falls back to "Alex sine videoer" offline).
- One window, one big button: **Hent nye videoer**, with a progress bar and
  a status line below. While downloading, the same button turns into a red
  **Stopp** that cancels the run ("Stoppet. N videoer ble lagret.").
- At the bottom: a two-way toggle **På PC-en / På minnepinne** for where
  videos are saved (remembered), and an **Åpne videomappen** button that
  opens the target folder in Explorer.
- Done: "Ferdig! N nye videoer lagret."
- Errors (network down etc.): "Noe gikk galt, prøv igjen senere" plus the
  count that succeeded. Failed videos are not archived, so the next run
  retries them.

## Technical

- **Channels:** `channels.txt` in the repo, fetched from GitHub on every run;
  the local copy next to the exe is the offline fallback, and a baked-in
  default list (`https://www.youtube.com/@AlexSkoog-ks1pl`) is the last
  resort.
- **Target folder:** a two-way choice stored in `folder.txt` next to the
  exe: "pc" (default) saves to `~/Videos`, "usb" saves to the first removable
  drive (GetDriveType == DRIVE_REMOVABLE); a friendly message asks for the
  stick if none is inserted. Videos land directly in the target folder.
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
