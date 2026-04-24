import ctypes
import os
import threading
import time
import tkinter as tk

from gtts import gTTS
from pycaw.pycaw import AudioUtilities


def set_apps_mute(mute_status):
    """Mute/Unmute semua apps kecuali Python"""
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name().lower() != "python.exe":
                interface.SetMute(mute_status, None)
    except:
        pass


def play_mp3_pro(path):
    """MCI Player - Bulletproof version"""
    path = os.path.abspath(path)
    ctypes.windll.winmm.mciSendStringW(
        f'open "{path}" type mpegvideo alias test_voice', None, 0, 0
    )
    ctypes.windll.winmm.mciSendStringW("play test_voice wait", None, 0, 0)
    ctypes.windll.winmm.mciSendStringW("close test_voice", None, 0, 0)


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
        root, text=teks, font=("Arial", 38, "bold"), fg="white", bg="#FF0033"
    )
    lbl.pack(expand=True)

    root.after(masa_saat * 1000, root.destroy)
    root.mainloop()


def speak_voice(
    text,
    lang_code="ms",
    papar_popup=True,
    teks_popup="GO TO YOUR PC NOW\nFrom your Husband",
):
    """Fungsi bercakap dengan sokongan teks popup kustom"""
    filename = "test_temp.mp3"
    print(f"\n[SISTEM BERCAKAP]: {text}")

    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filename)
    except Exception as e:
        print(f"Gagal jana suara: {e}")
        return

    set_apps_mute(1)
    time.sleep(1)

    if papar_popup:
        durasi_popup = 12 if lang_code == "en" else 4
        threading.Thread(target=tunjuk_popup, args=(teks_popup, durasi_popup)).start()

    play_mp3_pro(filename)

    time.sleep(1.5)
    set_apps_mute(0)

    if os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            pass


# --- INTRO ---
intro_english = (
    "Hi everyone, quick story I thought I’d share — my wife is now working from home, distractions are real. "
    "So instead of just reminding her the normal way, I decided to engineer a smarter, and slightly fun, solution. "
    "I built a lightweight Python script that runs silently in the background... no console, no interruptions... just clean automation. "
    "Using a dot p y w approach, it stays invisible while doing its job behind the scenes."
)

# --- TEST ---
test_list = [
    "Hai.. sudah breakfast ke, jom tengok pisi sekejap, update apa yang patut ya?",
    "Adilah.. dah sejam ni. Check lo-gin laptop tau, nanti bos cari pula.",
    "Reminder sejam sekali! Jom jengah kerja kejap, lepas tu boleh sambung rehat.",
    "Adilah.. check pisi jap, mana tahu ada email penting masuk dari bos.",
    "Adilah.. jangan lupa update kerja dekat pisi tu tau. Suami awak cakap, ai luv yu!",
    "Jom lo-gin jap Adilah.. tunjuk muka sikit dekat sistem kerja tu.",
]

print("--- MEMULAKAN QC SUARA & VISUAL DILLA (DEMO EDITION) ---")

print("\nSedia untuk record... Sistem akan bermula dalam:")
for i in range(10, 0, -1):
    print(f"{i} saat...")
    time.sleep(1)

speak_voice(
    intro_english, lang_code="en", papar_popup=True, teks_popup="Hi All, this Just test"
)

for i, ayat in enumerate(test_list, 1):
    print("\n[Menunggu 10 saat sebelum ayat seterusnya...]")
    time.sleep(10)
    speak_voice(
        ayat,
        lang_code="ms",
        papar_popup=True,
        teks_popup="GO TO YOUR PC NOW\nFrom your Husband",
    )

print("\n--- DEMO SELESAI! ---")
