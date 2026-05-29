# Bad Apple!! - PyScript Web

A browser-based, pure-Python implementation of the classic "Bad Apple!!" touhou animation. This project runs entirely on the client side without needing a backend server, utilizing **PyScript** and **WebAssembly (WASM)** to render and synchronize ASCII frames in real-time.

## 🚀 Features

* **Pure Python Frontend:** No JavaScript used for playback logic. The entire DOM manipulation and synchronization engine is written in Python via `PyScript`.
* **Perfect Audio Synchronization:** Uses a master absolute clock based on the native HTML5 audio timer to ensure frames never drift from the music.
* **Smart Responsive Scaling:** Dynamically calculates aspect ratios to support edge-to-edge rendering on Desktop (Landscape) and letterboxing on Mobile (Portrait) without distortion.
* **Zero Backend:** Because the video data is pre-compiled into a JSON file, this project can be hosted completely for free on static site hosts like GitHub Pages.

## 🛠️ Tech Stack

* **Python 3** (via PyScript & Pyodide)
* **HTML5 / CSS3** (Flexbox & Viewport scaling)
* **OpenCV / NumPy** (Used locally for pre-rendering the video data)

## 📁 How It Works

1. **The Compiler (`generate.py`):** A local Python script that uses OpenCV and NumPy to process the original `bad_apple.mp4` video frame-by-frame. It thresholds the video into pure black-and-white ASCII (`█` and spaces) and exports it into a highly optimized `frames.json` file.
2. **The Player (`main.py` & `index.html`):** The static website loads the PyScript engine. The Python script fetches the JSON data, buffers the `bad_apple.mp3` audio, and uses `asyncio` to drive a 60Hz loop that injects the exact correct text frame into the DOM based on the audio's current timestamp.

## ⚠️ Disclaimer

This project is for educational purposes only. The music, video, and text representations are the property of their respective owners.
