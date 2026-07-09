# Alex Videoer

One-button Windows app that downloads new videos from fixed YouTube channels
to the PC (`~/Videos`) or a USB stick, a remembered two-way toggle. The same
button stops an ongoing run. The UI is in Norwegian; Alex is the end user.
Design: `docs/superpowers/specs/2026-07-05-alex-videoer-design.md`.

## Build and deliver

Every push to `main` builds `Alex Videoer.exe` plus an installer
(`AlexVideoerSetup.exe`) and publishes a GitHub release (v1, v2, ...).

## First install on Alex's PC (no scary dialogs)

SmartScreen's "unknown publisher" dialog only fires on files that carry
mark-of-the-web, which only a browser download adds. Alex's copy never has
it: the first install arrives on a USB stick, and every later update is
written by the app itself; neither path carries the mark. The warning you
see when downloading the exe from GitHub on a Windows machine stays on that
machine.

Setup checklist:

1. Copy `AlexVideoerSetup.exe` from Releases onto a FAT32 or exFAT USB
   stick (these filesystems cannot store mark-of-the-web).
2. Run it on his PC: installs per-user (no admin/UAC prompt), creates
   desktop and Start Menu shortcuts, starts the app.
3. In an admin PowerShell, exclude the app folder from Defender so a future
   build can never be false-positive quarantined (unsigned PyInstaller exes
   occasionally trip AV heuristics on new definition updates):
   `Add-MpPreference -ExclusionPath "C:\Users\<alex>\AppData\Local\Programs\Alex Videoer"`
4. Newer Windows 11 installs may have Smart App Control on (Settings >
   Privacy & security > Windows Security > App & browser control), which
   blocks unsigned apps regardless of mark-of-the-web. If it is On, turn it
   off during setup (one-way switch, so decide deliberately). Windows 10
   does not have it, and it only ships enabled on fresh Windows 11 installs.

No physical access to the PC: run the same checklist over Quick Assist
(built into Windows 10 and 11; Alex or a helper reads you a 6-digit code
and clicks Allow, then you drive). Downloading the installer during that
session shows the SmartScreen warning to you, not him; click through it,
install, and updates are silent from then on. Never send Alex a download
link; the browser download is the only path that shows the warning.

Why not code signing: Microsoft's Artifact Signing (formerly Trusted
Signing) only onboards individuals in US/Canada and organizations in
US/CA/EU/UK, and through 2026 has had recurring SmartScreen regressions
even for paying customers (Azure/artifact-signing-action#128). Classic
OV/EV certificates cost $200-450/year and still warn until reputation
builds per release. The USB + self-update flow above needs none of it.

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
