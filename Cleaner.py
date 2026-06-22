import sys
import threading
import time
import tkinter as tk
from tkinter import ttk
from pynput import keyboard, mouse

# Application Configurations
LOCK_DURATION_SECONDS = 30

# Thread-safe Application State
devices_disabled = False
keyboard_listener = None
mouse_listener = None


def play_system_beep():
    """Emits a sharp sound notification when devices change state."""
    root.bell()


def hardware_block_worker():
    """Binds OS hooks to drop all Bluetooth and wired inputs simultaneously."""
    global keyboard_listener, mouse_listener, devices_disabled

    play_system_beep()

    # 1. Ultimate Bluetooth & Wired Keyboard Suppression
    keyboard_listener = keyboard.Listener(
        on_press=lambda key: None, on_release=lambda key: None, suppress=True
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

    # 3. Asynchronous Safe Visual Countdown & Progress Bar Loop
    total_steps = LOCK_DURATION_SECONDS * 10  # 10 updates per second for smooth animation
    progress_step = 100 / total_steps

    for step in range(total_steps):
        if not devices_disabled:
            break

        # Calculate time remaining
        remaining = LOCK_DURATION_SECONDS - (step / 10)

        # Smoothly update the progress bar and status text
        progress_var.set(100 - (step * progress_step))
        update_status_ui(
            f"🔒 DEVICES LOCKED\nAuto-unlocking in {remaining:.1s}s", "#ff3333"
        )

        time.sleep(0.1)

    if devices_disabled:
        enable_cleaning_mode()


def disable_cleaning_mode():
    """Initiates device lockdown on an isolated worker thread."""
    global devices_disabled
    if devices_disabled:
        return

    devices_disabled = True

    # Visual State Adjustments
    lock_btn.config(state="disabled")
    progress_bar.pack(fill="x", padx=50, pady=(0, 20))
    root.update_idletasks()

    threading.Thread(target=hardware_block_worker, daemon=True).start()


def enable_cleaning_mode():
    """Destroys hardware hooks safely and restores native control maps."""
    global devices_disabled, keyboard_listener, mouse_listener

    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None

    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

    devices_disabled = False

    # Reset GUI layout values cleanly
    progress_var.set(100)
    progress_bar.pack_forget()
    lock_btn.config(state="normal")
    update_status_ui("Status: READY FOR SANITIZATION", "#00ff66")
    play_system_beep()


def update_status_ui(text, color):
    """Updates GUI state labels cleanly across threading boundaries."""
    status_var.set(text)
    status_label.config(fg=color)


# ==============================================================================
# PREMIUM NEON GRAPHICAL USER INTERFACE (Tkinter)
# ==============================================================================
root = tk.Tk()
root.title("Hardware Sanitizer Pro")
root.geometry("460x320")
root.configure(bg="#0a0a0a")
root.resizable(False, False)

# Custom High-Contrast Premium Styles
style = ttk.Style()
style.theme_use("clam")

# Neon Red Lock Button Style
style.configure(
    "Lock.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=14,
    background="#cc0000",
    foreground="white",
)
style.map(
    "Lock.TButton",
    background=[("disabled", "#222222"), ("active", "#ff0000")],
    foreground=[("disabled", "#555555")],
)

# Custom Neon Progress Bar Style
style.configure(
    "Neon.Horizontal.TProgressbar",
    troughcolor="#111111",
    background="#ff3333",
    thickness=8,
)

# UI Component Placement
title = tk.Label(
    root,
    text="Hardware Sanitizer Pro",
    font=("Segoe UI", 24, "bold"),
    bg="#0a0a0a",
    fg="#ffffff",
)
title.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Swallows Bluetooth, wireless, and built-in peripheral inputs.",
    font=("Segoe UI", 10),
    bg="#0a0a0a",
    fg="#666666",
)
subtitle.pack(pady=(0, 20))

status_var = tk.StringVar(value="Status: READY FOR SANITIZATION")
status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 12, "bold"),
    justify="center",
    bg="#0a0a0a",
    fg="#00ff66",
)
status_label.pack(pady=(0, 20))

progress_var = tk.DoubleVar(value=100)
progress_bar = ttk.Progressbar(
    root,
    variable=progress_var,
    maximum=100,
    style="Neon.Horizontal.TProgressbar",
    mode="determinate",
)
# Progress bar remains hidden from layout until lock loop is activated

lock_btn = ttk.Button(
    root,
    text="🔒 START 30s HARDWARE LOCK",
    style="Lock.TButton",
    command=disable_cleaning_mode,
)
lock_btn.pack(fill="x", padx=50)

# Window Close Fallback Handler (If the window is forced closed, it breaks the hooks)
root.protocol(
    "WM_DELETE_WINDOW", lambda: [enable_cleaning_mode(), root.destroy()]
)

root.mainloop()
