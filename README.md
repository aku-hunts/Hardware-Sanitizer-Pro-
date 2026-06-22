# Hardware Sanitizer Pro

Hardware Sanitizer Pro is a lightweight utility designed to temporarily disable keyboard, mouse, and trackpad input while you clean your device. Whether you're wiping down your keyboard, cleaning a laptop trackpad, or dusting your mouse, the application helps prevent accidental key presses, clicks, shortcuts, and unwanted system actions.

Built with Python and Tkinter, the tool provides a simple interface while running input suppression in the background. A built-in countdown timer automatically restores control after a cleaning session, ensuring you never remain locked out of your computer.

## Features

* Keyboard input suppression
* Mouse and trackpad locking
* Support for wired and wireless peripherals
* Automatic unlock countdown
* Clean and lightweight Tkinter interface
* Background-threaded operation
* Fail-safe recovery system
* Open-source and easy to modify

## Installation

1. Clone or download the project.
2. Install the required dependency:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install pynput
```

## Running

### Windows

```bash
python main.py
```

### Linux

```bash
sudo python3 main.py
```

### macOS

```bash
sudo python3 main.py
```

Note: Some operating systems may require elevated permissions for input interception.

## How to Use

1. Launch the application.
2. Press the lock button.
3. Clean your keyboard, mouse, or trackpad.
4. Wait for the countdown to finish.
5. Input devices are automatically restored.

## Requirements

* Python 3.8+
* pynput 1.7.6+

## Project Structure

```text
Hardware-Sanitizer-Pro/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Disclaimer

This software is provided for convenience and educational purposes. Input suppression behavior may vary depending on operating system limitations, permissions, and connected hardware. Always test the application before relying on it for critical use.

## License

Released under the MIT License. See the LICENSE file for more information.
