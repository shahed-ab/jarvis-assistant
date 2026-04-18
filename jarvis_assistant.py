"""
J.A.R.V.I.S Clap Assistant
===========================
Clap twice → Chrome & VS Code open automatically.

Requirements:
    pip install pyaudio numpy

On Linux also run:
    sudo apt-get install portaudio19-dev python3-pyaudio

Usage:
    python jarvis_assistant.py
"""

import sys
import time
import threading
import subprocess
import platform
import os

# ──────────────────────────────────────────────
# Try importing audio libs with friendly errors
# ──────────────────────────────────────────────
try:
    import pyaudio
    import numpy as np
except ImportError:
    print("=" * 55)
    print("  J.A.R.V.I.S  –  Missing Dependencies")
    print("=" * 55)
    print("\n  Please install required packages:\n")
    print("    pip install pyaudio numpy\n")
    print("  On Linux you may also need:")
    print("    sudo apt-get install portaudio19-dev\n")
    sys.exit(1)

# ──────────────────────────────────────────────
# Configuration  (tweak to your environment)
# ──────────────────────────────────────────────
CLAP_THRESHOLD   = 2500   # Amplitude threshold – raise if too sensitive
CLAP_COOLDOWN    = 0.15   # Seconds to ignore audio right after a clap (debounce)
DOUBLE_CLAP_GAP  = 1.2    # Max seconds between two claps to count as "double"

SAMPLE_RATE  = 44100
CHUNK_SIZE   = 1024
CHANNELS     = 1
FORMAT       = pyaudio.paInt16

OS = platform.system()  # 'Windows', 'Darwin', 'Linux'

# ──────────────────────────────────────────────
# App launch commands per OS
# ──────────────────────────────────────────────
def get_commands():
    if OS == "Windows":
        chrome  = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        vscode  = r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(
                      os.environ.get("USERNAME", "User"))
        return [chrome], [vscode]

    elif OS == "Darwin":   # macOS
        chrome = ["open", "-a", "Google Chrome"]
        vscode = ["open", "-a", "Visual Studio Code"]
        return chrome, vscode

    else:                  # Linux
        chrome = ["google-chrome"]          # or "chromium-browser"
        vscode = ["code"]
        return chrome, vscode


def launch_apps():
    chrome_cmd, vscode_cmd = get_commands()
    print("\n  🚀  Launching Google Chrome & VS Code …\n")
    try:
        if OS == "Windows":
            subprocess.Popen(chrome_cmd[0])
            subprocess.Popen(vscode_cmd[0])
        else:
            subprocess.Popen(chrome_cmd)
            subprocess.Popen(vscode_cmd)
        print("  ✅  Apps launched successfully!\n")
    except FileNotFoundError as e:
        print(f"  ⚠️  Could not find app: {e}")
        print("  Edit the paths in get_commands() to match your system.\n")


# ──────────────────────────────────────────────
# HUD – terminal visualiser
# ──────────────────────────────────────────────
IRON_MAN_BANNER = r"""
  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║    ░░░   J . A . R . V . I . S   ░░░            ║
  ║    Just A Rather Very Intelligent System         ║
  ║                                                  ║
  ║    [ CLAP DETECTION MODULE  –  ONLINE ]          ║
  ║                                                  ║
  ╚══════════════════════════════════════════════════╝

  🎤  Listening for double-clap …
  👏  Clap  →  Clap  (within {gap}s)  →  Apps launch

  Press  Ctrl+C  to shut down
  ─────────────────────────────────────────────────
""".format(gap=DOUBLE_CLAP_GAP)


def animate_listening():
    """Prints a simple pulsing dot animation in a separate thread."""
    symbols = ["◉ ", "○ ", "◉ ", "○ "]
    i = 0
    while _running:
        sys.stdout.write(f"\r  {symbols[i % len(symbols)]} Monitoring audio …  ")
        sys.stdout.flush()
        i += 1
        time.sleep(0.5)


# ──────────────────────────────────────────────
# Core clap detection loop
# ──────────────────────────────────────────────
_running = True

def detect_claps():
    global _running

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    last_clap_time   = 0
    first_clap_time  = 0
    clap_count       = 0
    in_silence       = True   # tracks whether we were silent before this chunk

    try:
        while _running:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude  = np.max(np.abs(audio_data))

            now = time.time()

            # Detect rising edge: silence → loud (avoids counting sustained sound)
            if amplitude > CLAP_THRESHOLD and in_silence:
                in_silence = False  # we are now inside a loud burst

                # Ignore if within debounce window
                if now - last_clap_time < CLAP_COOLDOWN:
                    continue

                time_since_first = now - first_clap_time

                if clap_count == 0:
                    # First clap
                    clap_count      = 1
                    first_clap_time = now
                    sys.stdout.write(f"\r  👏  Clap 1 detected! Waiting for clap 2 …          \n")
                    sys.stdout.flush()

                elif clap_count == 1 and time_since_first <= DOUBLE_CLAP_GAP:
                    # Second clap within window → LAUNCH!
                    clap_count = 0
                    sys.stdout.write(f"\r  👏👏  Double clap detected!                          \n")
                    sys.stdout.flush()
                    launch_apps()

                else:
                    # Too slow — treat this as a new first clap
                    clap_count      = 1
                    first_clap_time = now
                    sys.stdout.write(f"\r  👏  Clap 1 detected! (previous expired) …          \n")
                    sys.stdout.flush()

                last_clap_time = now

            elif amplitude <= CLAP_THRESHOLD:
                in_silence = True   # back to silence, ready for next rising edge

            # Reset if first clap window has expired without a second clap
            if clap_count == 1 and (now - first_clap_time) > DOUBLE_CLAP_GAP:
                clap_count = 0
                sys.stdout.write(f"\r  ⏱  Clap window expired. Try again …                 \n")
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        _running = False
        stream.stop_stream()
        stream.close()
        p.terminate()


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print(IRON_MAN_BANNER)

    # Start animation thread
    anim_thread = threading.Thread(target=animate_listening, daemon=True)
    anim_thread.start()

    # Run clap detection (blocks until Ctrl+C)
    detect_claps()

    print("\n\n  ⬛  J.A.R.V.I.S offline.  Goodbye.\n")
