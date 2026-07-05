"""Self-check: downloads the newest video (low quality) twice, verifies the archive."""

import glob
import os
import shutil
import tempfile
import threading

import yt_dlp

import alex_videoer

alex_videoer.FORMAT = "worst"  # small file; the production format is not tested here

channel = alex_videoer.load_channels()[0]
with yt_dlp.YoutubeDL(
    {"extract_flat": True, "playlist_items": "1", "quiet": True}
) as ydl:
    info = ydl.extract_info(channel.rstrip("/") + "/videos", download=False)
video_url = list(info["entries"])[0]["url"]
print("Test video:", video_url)

dest = tempfile.mkdtemp(prefix="alexdl")
try:
    cancel = threading.Event()
    cancel.set()  # pre-set: the first hook call must abort the run
    n0, ok0 = alex_videoer.download_new_videos(dest, [video_url], print, cancel)
    assert ok0 and n0 == 0, (n0, ok0)

    n, ok = alex_videoer.download_new_videos(dest, [video_url], print)
    assert ok and n == 1, (n, ok)
    files = glob.glob(os.path.join(dest, "*", "*.*"))
    assert files, "no file downloaded"
    assert os.path.exists(os.path.join(dest, ".downloaded.txt"))

    n2, ok2 = alex_videoer.download_new_videos(dest, [video_url], print)
    assert ok2 and n2 == 0, (n2, ok2)
    print(f"OK: {files[0]} ({os.path.getsize(files[0])} bytes), second run skipped it.")
finally:
    shutil.rmtree(dest)
