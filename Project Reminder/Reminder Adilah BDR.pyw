import os
import sys

# --- Security IqwanEngine ---
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# IqwanEngine
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------

import ctypes
import random
import threading
import time
import tkinter as tk
from datetime import datetime

from gtts import gTTS
from pycaw.pycaw import AudioUtilities


def set_apps_mute(mute_status):
    """Mute/Unmute semua aplikasi (Chrome, YouTube, dll) kecuali Python"""
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name().lower() != "python.exe":
                interface.SetMute(mute_status, None)
    except Exception as e:
        print(f"Error pada sistem mute: {e}")


def play_mp3_pro(path):
    """Mainkan file MP3 guna Windows MCI (Media Control Interface)"""
    path = os.path.abspath(path)
    ctypes.windll.winmm.mciSendStringW(
        f'open "{path}" type mpegvideo alias nisa_voice', None, 0, 0
    )
    ctypes.windll.winmm.mciSendStringW("play nisa_voice wait", None, 0, 0)
    ctypes.windll.winmm.mciSendStringW("close nisa_voice", None, 0, 0)


def tunjuk_popup(teks, masa_saat):
    """Bina popup amaran besar di tengah skrin"""
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    root.configure(bg="#FF0033", highlightbackground="white", highlightthickness=8)

    w, h = 900, 200
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw / 2) - (w / 2)
    y = (sh / 2) - (h / 2)
    root.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")

    lbl = tk.Label(
        root, text=teks, font=("Arial", 45, "bold"), fg="white", bg="#FF0033"
    )
    lbl.pack(expand=True)

    root.after(masa_saat * 1000, root.destroy)
    root.mainloop()


def speak_malay(text):
    """Proses utama: Mute -> Bina Suara -> Popup & Cakap -> Unmute"""
    filename = "voice_temp_main.mp3"

    try:
        tts = gTTS(text=text, lang="ms")
        tts.save(filename)

        set_apps_mute(1)
        time.sleep(2)

        amaran_visual = "GO TO YOUR PC NOW\nFrom your Husband!"
        threading.Thread(target=tunjuk_popup, args=(amaran_visual, 3)).start()

        print(f"[{datetime.now().strftime('%H:%M:%S')}] PC sedang cakap: {text}")
        play_mp3_pro(filename)

        time.sleep(2)
        set_apps_mute(0)

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print(f"Ralat dalam speak_malay: {e}")
        set_apps_mute(0)


# --- Listing ---
pesanan_random = [
    "Hai.. sudah breakfast ke, jom tengok pisi sekejap, update apa yang patut ya?",
    "Adilah.. dah sejam ni. Check lo-gin laptop tau, nanti bos cari pula.",
    "Reminder sejam sekali! Jom jengah kerja kejap, lepas tu boleh sambung rehat.",
    "Adilah.. check pisi jap, mana tahu ada email penting masuk dari bos.",
    "Adilah.. jangan lupa update kerja dekat pisi tu tau. Suami awak cakap, ai luv yu!",
    "Jom lo-gin jap Adilah.. tunjuk muka sikit dekat sistem kerja tu.",
]

print("--- SISTEM REMINDER DILLA BDR (STABLE VERSION) ---")

# --- Starting ---
speak_malay(
    "Testing satu dua tiga. Hello Adilah, saya sudah sedia untuk ingatkan awak esok dan saya sediakan beberapa pesanan dari suami awak encik Iqwan!"
)

while True:
    now = datetime.now()
    h = now.hour
    m = now.minute

    if h == 8 and m == 0:
        pesanan_pagi = "Hello.. gud morning Adilah. Jangan lupa lo-gin laptop untuk kerja ya. Semangat sikit hari ni!"
        speak_malay(pesanan_pagi)
        time.sleep(61)

    elif 9 <= h <= 16 and m == 0:
        pesanan_jam = random.choice(pesanan_random)
        speak_malay(pesanan_jam)
        time.sleep(61)

    if h == 16 and m == 45:
        pesanan_balik = "Adilah.. dah nak balik ni. Boleh stand bye nak off pisi kerja. Suami awak cakap. Selamat Berehat dan jangan lupa memasak ya!"
        speak_malay(pesanan_balik)
        time.sleep(61)

    time.sleep(30)
