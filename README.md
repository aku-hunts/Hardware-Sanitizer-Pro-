# Hardware Sanitizer Pro

Hardware Sanitizer Pro is a compact Tkinter desktop app for cleaning your keyboard, mouse, trackpad, and connected peripherals without accidental input. It temporarily suppresses keyboard and pointer events for a fixed 30-second cleaning window, shows a live countdown, and restores input automatically when the timer ends.

The app uses a neon v2.0 interface and supports a bundled app icon at `assets/app_icon.png`.

## Features

- 30-second cleaning lock with automatic unlock.
- Global keyboard suppression through `pynput` while the lock is active.
- Mouse and trackpad suppression for movement, clicks, and scrolling.
- Support for wired, wireless, Bluetooth, RF, and other HID-style peripherals when the OS allows global hooks.
- Live countdown and progress bar.
- Window-close cleanup that stops active listeners before exiting.
- Clear error state if operating-system permissions block input hooks.
- Bundled keyboard-cleaner app icon.

## Safety and Permissions

Input suppression depends on your operating system, security settings, and desktop session. Test the app before depending on it, and never use it as a security or access-control lock.

Platform guidance:

- **Windows:** run normally first; if suppression is incomplete, run your terminal as Administrator.
- **macOS:** grant Accessibility/Input Monitoring permissions to Terminal, Python, or your IDE in System Settings.
- **Linux:** global hooks may require an X11 session and elevated privileges. Wayland sessions often restrict this type of input interception.

## Requirements

- Python 3.8 or newer
- Tkinter, included with most Python installers
- `pynput`, installed from `requirements.txt`
- `pyinstaller`, only needed if you want to build the app/executable

## Installation

```bash
python -m pip install -r requirements.txt
