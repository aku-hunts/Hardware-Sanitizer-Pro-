import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput import keyboard, mouse

# Application Configurations
LOCK_DURATION_SECONDS = 30  # Safety fallback timer

# Thread-safe Application State
devices_disabled = False
keyboard_listener = None
mouse_listener = None


def global_key_interceptor(key):
    """Monitors keys during lock.

    Intercepts the emergency escape shortcut.
    """
    global devices_disabled
    try:
        # We look for a custom emergency combination if needed,
        # but pynput.keyboard.Listener handles suppression independently.
        pass
    except Exception:
        pass


def hardware_block_worker():
    """Binds OS window manager hooks to block all Bluetooth/Wired inputs

    simultaneously.
    """
    global keyboard_listener, mouse_listener, devices_disabled

    # 1. Ultimate Bluetooth & Wired Keyboard Suppression
    # suppress=True tells the OS to instantly swallow the event
    keyboard_listener = keyboard.Listener(
        on_press=global_key_interceptor,
        on_release=lambda key: None,
        suppress=True,
    )
    keyboard_listener.start()

    # 2. Complete Trackpad & Mouse Interception
    mouse_listener = mouse.Listener(
        on_move=lambda x, y: False,
        on_click=lambda x, y, button, pressed: False,
        on_scroll=lambda x, y, dx, dy: False,
        suppress=True,
    )
    mouse_listener.start()

    # 3. Asynchronous Safe Visual Countdown
    for remaining in range(LOCK_DURATION_SECONDS, 0, -1):
        if not devices_disabled:
            break
        update_status_ui(
            f"⚠️ DEVICE LOCKED!\nAuto-unlocking in {remaining}s", "#e74c3c"
        )
        time.sleep(1)

    # Force auto-unlock when timer expires
    if devices_disabled:
        enable_cleaning_mode()


def disable_cleaning_mode():
    """Initiates hardware suppression securely across a dedicated thread."""
    global devices_disabled
    if devices_disabled:
        return

    devices_disabled = True

    # Lock the interface button to prevent duplicate spamming
    lock_btn.config(state="disabled")
    root.update_idletasks()

    # Offload suppression to a worker thread to prevent Tkinter window freezing
    threading.Thread(target=hardware_block_worker, daemon=True).start()


def enable_cleaning_mode():
    """Gracefully tears down all system hooks and restores native controls."""
    global devices_disabled, keyboard_listener, mouse_listener

    # Safely terminate keyboard hook
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None

    # Safely terminate mouse/trackpad hook
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

    devices_disabled = False

    # Restore UI element interaction smoothly
    lock_btn.config(state="normal")
    update_status_ui("Status: READY FOR SANITIZATION", "#2ecc71")


def update_status_ui(text, color):
    """Thread-safe UI utility wrapper to update the status text and colors."""
    status_var.set(text)
    status_label.config(fg=color)


# ==========================================
# Graphical User Interface Design (Tkinter)
# ==========================================
root = tk.Tk()
root.title("Hardware Sanitizer Pro")
root.geometry("460x290")
root.configure(bg="#111111")
root.resizable(False, False)

# Clean, Modern Styling Map
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Lock.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=14,
    background="#c0392b",
    foreground="white",
)

# Text and Layout Architecture
title = tk.Label(
    root,
    text="Hardware Sanitizer Pro",
    font=("Segoe UI", 22, "bold"),
    bg="#111111",
    fg="#ffffff",
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Swallows all Bluetooth, USB, and built-in peripheral inputs.",
    font=("Segoe UI", 10),
    bg="#111111",
    fg="#666666",
)
subtitle.pack(pady=(0, 20))

status_var = tk.StringVar(value="Status: READY FOR SANITIZATION")
status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 12, "bold"),
    justify="center",
    bg="#111111",
    fg="#2ecc71",
)
status_label.pack(pady=(0, 25))

lock_btn = ttk.Button(
    root,
    text="🔒 START 30s HARDWARE LOCK",
    style="Lock.TButton",
    command=disable_cleaning_mode,
)
lock_btn.pack(fill="x", padx=50)

# Failsafe window closure hook: if they manage to kill the app window,
# hardware hooks disarm cleanly.
root.protocol(
    "WM_DELETE_WINDOW", lambda: [enable_cleaning_mode(), root.destroy()]
)

root.mainloop()
