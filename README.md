# 👏 J.A.R.V.I.S Clap Assistant

> **Just A Rather Very Intelligent System** — Clap twice and watch Chrome & VS Code launch automatically, Iron Man style.

---

## ✨ Features

- 👏 **Double-clap detection** via your microphone
- 🚀 **Auto-launches** Google Chrome & VS Code instantly
- 🖥️ **Cross-platform** — Works on Windows, macOS & Linux
- 🎛️ **Fully customizable** — Tune sensitivity, timing, and target apps
- 🔒 **100% local** — No internet, no data sent anywhere

---

## 📸 Demo

```
  ╔══════════════════════════════════════════════════╗
  ║    ░░░   J . A . R . V . I . S   ░░░            ║
  ║    Just A Rather Very Intelligent System         ║
  ║    [ CLAP DETECTION MODULE  –  ONLINE ]          ║
  ╚══════════════════════════════════════════════════╝

  👏  Clap 1 detected! Waiting for clap 2 …
  👏👏  Double clap detected!
  🚀  Launching Google Chrome & VS Code …
  ✅  Apps launched successfully!
```

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/shahed-ab/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Install dependencies

**Windows / macOS:**
```bash
pip install pyaudio numpy
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio numpy
```

**macOS (if pyaudio fails):**
```bash
brew install portaudio
pip install pyaudio numpy
```

---

## ▶️ Usage

```bash
python jarvis_assistant.py
```

Then **clap twice** 👏👏 within 1.2 seconds — Chrome and VS Code will open automatically!

To stop, press **Ctrl + C**.

---

## ⚙️ Configuration

You can tweak these settings at the top of `jarvis_assistant.py`:

| Setting | Default | Description |
|---|---|---|
| `CLAP_THRESHOLD` | `2500` | Mic sensitivity — raise if too many false triggers |
| `CLAP_COOLDOWN` | `0.15s` | Debounce time after each clap |
| `DOUBLE_CLAP_GAP` | `1.2s` | Max time between two claps |

---

## 📋 Requirements

- Python 3.7+
- `pyaudio`
- `numpy`

---

## 🖥️ Platform Support

| OS | Status |
|---|---|
| Windows | ✅ Supported |
| macOS | ✅ Supported |
| Linux | ✅ Supported |

---

## 📁 Project Structure

```
jarvis-assistant/
├── jarvis_assistant.py   # Main script
├── requirements.txt      # Dependencies
└── README.md             # You are here
```

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or want to add a feature (like voice feedback or custom app launching), feel free to open an issue.

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ inspired by Iron Man's J.A.R.V.I.S</p>
