# Alex Videoer

One-button Windows app that downloads new videos from fixed YouTube channels
to the PC (`~/Videos`) or a USB stick, a remembered two-way toggle. The same
button stops an ongoing run. The UI is in Norwegian; Alex is the end user.
Design: `docs/superpowers/specs/2026-07-05-alex-videoer-design.md`.

## Build and deliver

Every push to `main` builds `Alex Videoer.exe` plus an installer
(`AlexVideoerSetup.exe`) and publishes a GitHub release (v1, v2, ...).
First delivery: download `AlexVideoerSetup.exe` from Releases and hand it
over on a USB stick (FAT32/exFAT carries no mark-of-the-web, so SmartScreen
stays quiet). Running it installs the app per-user (no admin prompt) with a
desktop and Start Menu shortcut, then starts it.

The exe is unsigned, so a copy downloaded straight from the internet gets a
SmartScreen "unknown publisher" warning: click "More info" then "Run anyway"
(or right-click the file, Properties, Unblock). This is one-time; self-updates
do not retrigger it. Making the warning disappear entirely requires a code
signing certificate (e.g. Azure Trusted Signing, ~$10/month).

## Updates

The app checks for a new release at every startup and replaces itself
automatically. Pushing to `main` (or running the workflow manually, e.g. to
pick up a new yt-dlp when YouTube changes) is all it takes; Alex gets the
update the next time he opens the app.

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
