# Alex Videoer

One-button Windows app that downloads new videos from a fixed list of
YouTube channels to the PC or a USB stick. The UI is in Norwegian.

## Build

Every push to `main` builds the app and publishes a GitHub release with
three artifacts:

- `Alex Videoer.exe`: portable exe, self-updates from GitHub releases
- `AlexVideoerSetup.exe`: per-user installer with desktop and Start Menu
  shortcuts
- `Alex.Videoer.msix`: Microsoft Store package, built when the `MSIX_*`
  repo variables are set; Store builds are updated through the Store

## Changing channels

Edit `channels.txt` in the repo, one channel URL per line. The app fetches
the file from GitHub on every run (the local copy next to the exe is the
offline fallback).

## Local testing (macOS)

```sh
python3 -m venv .venv && .venv/bin/pip install "yt-dlp[default]" customtkinter
brew install deno python-tk
.venv/bin/python test_download.py                 # self-check
ALEX_DEST=/tmp/alexdl .venv/bin/python alex_videoer.py  # run the app (dev dest override)
```
