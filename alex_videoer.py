"""Alex Videoer: henter nye videoer fra faste YouTube-kanaler til minnepinne."""

import json
import os
import queue
import subprocess
import sys
import threading
import urllib.request

try:
    from _version import VERSION  # genereres av byggejobben
except ImportError:
    VERSION = 0

GITHUB_REPO = "didriksg/alex-download"
CHANNELS_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/channels.txt"
DEFAULT_CHANNELS = ["https://www.youtube.com/@AlexSkoog-ks1pl"]
FORMAT = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

FROZEN = getattr(sys, "frozen", False)
APP_DIR = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))


def load_channels():
    local = os.path.join(APP_DIR, "channels.txt")
    text = ""
    try:
        with urllib.request.urlopen(CHANNELS_URL, timeout=5) as r:
            text = r.read().decode("utf-8")
        try:
            with open(local, "w", encoding="utf-8") as f:
                f.write(text)
        except OSError:
            pass
    except Exception:
        try:
            with open(local, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            pass
    urls = [s.strip() for s in text.splitlines() if s.strip() and not s.startswith("#")]
    return urls or DEFAULT_CHANNELS


def find_usb_drives():
    if os.environ.get("ALEX_USB_DIR"):
        return [os.environ["ALEX_USB_DIR"]]
    if sys.platform == "win32":
        import ctypes

        k32 = ctypes.windll.kernel32
        bitmask = k32.GetLogicalDrives()
        return [
            f"{chr(65 + i)}:\\"
            for i in range(26)
            if bitmask & (1 << i) and k32.GetDriveTypeW(f"{chr(65 + i)}:\\") == 2
        ]
    # ponytail: macOS-gren kun for utvikling; sluttbrukeren er på Windows
    return [
        os.path.join("/Volumes", d)
        for d in os.listdir("/Volumes")
        if d != "Macintosh HD"
    ]


def download_new_videos(dest_root, channels, event_cb):
    """Laster ned nye videoer. Sender ("status", tekst)/("progress", 0..1) til
    event_cb. Returnerer (antall_nye, alt_gikk_bra)."""
    import yt_dlp

    videos_dir = os.path.join(dest_root, "Videoer")
    os.makedirs(videos_dir, exist_ok=True)
    done_ids = set()

    def hook(d):
        info = d.get("info_dict") or {}
        title = info.get("title") or ""
        if d["status"] == "downloading":
            event_cb(("status", f"Laster ned: {title}"))
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                event_cb(("progress", d.get("downloaded_bytes", 0) / total))
        elif d["status"] == "finished":
            if info.get("id"):
                done_ids.add(info["id"])
            event_cb(("status", f"Behandler: {title} ..."))
            event_cb(("progress", 1.0))

    opts = {
        "format": FORMAT,
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(videos_dir, "%(channel)s", "%(title)s.%(ext)s"),
        "download_archive": os.path.join(videos_dir, ".downloaded.txt"),
        "windowsfilenames": True,
        "ignoreerrors": True,
        "retries": 3,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "progress_hooks": [hook],
    }
    if FROZEN:
        opts["ffmpeg_location"] = sys._MEIPASS
        opts["js_runtimes"] = {"deno": {"path": os.path.join(sys._MEIPASS, "deno.exe")}}

    with yt_dlp.YoutubeDL(opts) as ydl:
        retcode = ydl.download(channels)
    return len(done_ids), retcode == 0


def check_for_update(event_cb):
    """Bytter ut kjørende exe med nyeste GitHub-release. Returnerer ny sti eller None."""
    if not FROZEN:
        return None
    exe = sys.executable
    try:
        os.remove(exe + ".gammel")
    except OSError:
        pass
    new = exe + ".ny"
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        with urllib.request.urlopen(url, timeout=5) as r:
            rel = json.load(r)
        if int(rel["tag_name"].lstrip("v")) <= VERSION:
            return None
        asset = next(a for a in rel["assets"] if a["name"].endswith(".exe"))
        event_cb(("status", "Laster ned oppdatering ..."))

        def report(blocks, bs, total):
            if total > 0:
                event_cb(("progress", min(blocks * bs / total, 1.0)))

        urllib.request.urlretrieve(asset["browser_download_url"], new, report)
        os.rename(exe, exe + ".gammel")
        os.rename(new, exe)
        return exe
    except Exception:
        try:
            os.remove(new)
        except OSError:
            pass
        return None


class App:
    def __init__(self, root):
        self.root = root
        self.msgs = queue.Queue()
        root.title("Alex Videoer")
        root.geometry("520x360")
        root.resizable(False, False)
        if FROZEN:
            root.iconbitmap(os.path.join(sys._MEIPASS, "icon.ico"))

        ctk.CTkLabel(
            root, text="Alex sine videoer", font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=(36, 4))
        ctk.CTkLabel(
            root,
            text="Nye videoer fra YouTube, rett på minnepinnen",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
        ).pack(pady=(0, 24))
        self.button = ctk.CTkButton(
            root,
            text="Hent nye videoer",
            font=ctk.CTkFont(size=20, weight="bold"),
            height=56,
            corner_radius=28,
            command=self.start,
            state="disabled",
        )
        self.button.pack(fill="x", padx=56)
        self.bar = ctk.CTkProgressBar(root, height=8)
        self.bar.set(0)
        self.bar.pack(fill="x", padx=56, pady=(24, 10))
        self.status = ctk.CTkLabel(root, text="Starter ...", wraplength=440)
        self.status.pack(padx=24)
        ctk.CTkButton(
            root,
            text="Åpne videomappen",
            font=ctk.CTkFont(size=13, underline=True),
            fg_color="transparent",
            text_color="gray60",
            hover=False,
            width=140,
            height=28,
            command=self.open_folder,
        ).pack(side="bottom", pady=(0, 14))
        self.drive_buttons = []
        root.after(150, self.poll)
        threading.Thread(target=self.update_worker, daemon=True).start()

    def update_worker(self):
        new_exe = check_for_update(self.msgs.put)
        if new_exe:
            self.msgs.put(("status", "Appen er oppdatert og starter på nytt ..."))
            subprocess.Popen([new_exe])
            self.msgs.put(("quit",))
        else:
            self.msgs.put(("ready",))

    def start(self):
        self.pick_drive(self.run)

    def open_folder(self):
        def action(drive):
            self.clear_drive_buttons()
            folder = os.path.join(drive, "Videoer")
            os.makedirs(folder, exist_ok=True)
            if sys.platform == "win32":
                os.startfile(folder)
            else:
                subprocess.run(["open", folder])

        self.pick_drive(action)

    def pick_drive(self, action):
        self.clear_drive_buttons()
        drives = find_usb_drives()
        if not drives:
            self.status.configure(
                text="Fant ingen minnepinne. Sett inn minnepinnen og prøv igjen."
            )
        elif len(drives) == 1:
            action(drives[0])
        else:
            self.status.configure(text="Fant flere minnepinner. Hvilken vil du bruke?")
            for d in drives:
                b = ctk.CTkButton(self.root, text=d, width=120, command=lambda d=d: action(d))
                b.pack(pady=3)
                self.drive_buttons.append(b)

    def clear_drive_buttons(self):
        for b in self.drive_buttons:
            b.destroy()
        self.drive_buttons = []

    def run(self, drive):
        self.clear_drive_buttons()
        self.button.configure(state="disabled")
        self.bar.set(0)
        self.status.configure(text="Ser etter nye videoer ...")
        threading.Thread(target=self.worker, args=(drive,), daemon=True).start()

    def worker(self, drive):
        try:
            n, ok = download_new_videos(drive, load_channels(), self.msgs.put)
            if not ok:
                text = f"Noe gikk galt. {n} videoer ble lagret. Prøv igjen senere."
            elif n == 0:
                text = "Ingen nye videoer denne gangen."
            else:
                text = f"Ferdig! {n} nye videoer lagret. Du kan trygt ta ut minnepinnen."
        except Exception:
            text = "Noe gikk galt. Sjekk internett og minnepinnen, og prøv igjen."
        self.msgs.put(("done", text))

    def poll(self):
        while not self.msgs.empty():
            kind, *rest = self.msgs.get_nowait()
            if kind == "status":
                self.status.configure(text=rest[0])
            elif kind == "progress":
                self.bar.set(rest[0])
            elif kind == "ready":
                self.button.configure(state="normal")
                self.status.configure(text="Sett inn minnepinnen og trykk på knappen.")
            elif kind == "done":
                self.button.configure(state="normal")
                self.bar.set(0)
                self.status.configure(text=rest[0])
            elif kind == "quit":
                self.root.destroy()
                return
        self.root.after(150, self.poll)


if __name__ == "__main__":
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    App(root)
    root.eval("tk::PlaceWindow . center")
    root.mainloop()
