"""Selvtest: laster ned nyeste video (lav kvalitet) to ganger, sjekker arkivet."""

import glob
import os
import shutil
import tempfile

import yt_dlp

import alex_videoer

alex_videoer.FORMAT = "worst"  # liten fil; produksjonsformatet testes ikke her

channel = alex_videoer.load_channels()[0]
with yt_dlp.YoutubeDL(
    {"extract_flat": True, "playlist_items": "1", "quiet": True}
) as ydl:
    info = ydl.extract_info(channel.rstrip("/") + "/videos", download=False)
video_url = list(info["entries"])[0]["url"]
print("Testvideo:", video_url)

dest = tempfile.mkdtemp(prefix="alexusb")
try:
    n, ok = alex_videoer.download_new_videos(dest, [video_url], print)
    assert ok and n == 1, (n, ok)
    files = glob.glob(os.path.join(dest, "Videoer", "*", "*.*"))
    assert files, "ingen fil lastet ned"
    assert os.path.exists(os.path.join(dest, "Videoer", ".downloaded.txt"))

    n2, ok2 = alex_videoer.download_new_videos(dest, [video_url], print)
    assert ok2 and n2 == 0, (n2, ok2)
    print(f"OK: {files[0]} ({os.path.getsize(files[0])} bytes), andre kjøring hoppet over.")
finally:
    shutil.rmtree(dest)
