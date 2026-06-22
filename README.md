# Hardware Sanitizer Pro 🧼💻

Hardware Sanitizer Pro is a lightweight, open-source utility designed to temporarily lock down input peripherals on your computer. It allows you to safely wipe down, spray, and sanitize your keyboard, mouse, and laptop trackpad without triggering phantom keystrokes, accidental clicks, or system execution errors. 

By intercepting inputs at the OS kernel level, it acts as a digital shield for your machine during physical maintenance.

---

## Key Features 🌟

* **Total Peripheral Lockout**: Suppresses all standard keys, modifier combinations, mouse movements, trackpad gestures, scrolling, and physical clicks.
* **Smart Auto-Unlock Countdown**: An automated 30-second security timer ensures your system gracefully restores native input control even if you step away.
* **Emergency Escape Route**: Built-in global hotkey breakthrough (`Ctrl + Shift + U`) allows you to immediately bypass active mouse-locking and regain manual control instantly.
* **Thread-Isolated UI**: The asynchronous background execution architecture keeps the visual display alive, fluid, and responsive while hardware layers are frozen.
* **Failsafe Window Protocol**: Automatically disarms all low-level operational hooks if the interface window is suddenly terminated, ensuring your system never ends up stuck.

---

## Installation & Setup 🛠️

### 1. Prerequisites
Make sure you have [Python 3.8+](https://python.org) installed on your machine.

### 2. Clone or Download the Project
Download the repository files to your local machine:
```bash
git clone https://github.com
cd hardware-sanitizer-pro
```

### 3. Install Dependencies
This project utilizes external system hooks requiring the `keyboard` and `pynput` libraries. Install them via your terminal:
```bash
pip install -r requirements.txt
```
*(If you do not have a requirements file, simply run: `pip install keyboard pynput`)*

---

## How To Run 🚀

Because this tool hooks directly into low-level operating system input streams to manage hardware suppression, it **must** be executed with elevated administrative privileges.

### 🪟 Windows
1. Open your terminal or Command Prompt **as Administrator** (Right-click -> Run as Administrator).
2. Execute the script:
   ```bash
   python main.py
   ```

### 🐧 Linux & 🍏 macOS
Launch the script utilizing the `sudo` boundary prefix to allow kernel hook bindings:
```bash
sudo python3 main.py
```

---

## Technical Architecture ⚙️

The software utilizes a dual-layer interception architecture to reliably achieve input suppression:
1. **System Hook Interception**: Uses low-level operating system hooks to capture and drop keyboard events (`keyboard.suppress`) before they reach the window manager loop.
2. **Event Loop Truncation**: Leverages `pynput` to spawn an isolated background thread that listens to mouse/trackpad events and explicitly returns `False`, neutralizing inputs safely at the driver callback boundary.

---

## License 📄

This project is licensed under the **MIT License**. 

```text
Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
