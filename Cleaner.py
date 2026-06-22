"""Hardware Sanitizer Pro v2.0.

Single-file Tkinter app that suppresses keyboard, mouse, and trackpad input
while you clean your hardware. The lock lasts exactly 30 seconds.

Requires: pip install pynput

Platform notes:
  macOS   -> System Settings > Privacy & Security > Accessibility: grant
             Terminal, Python, or your IDE access before running.
  Linux   -> global input suppression may require X11 and elevated privileges.
  Windows -> run as Administrator if HID suppression is incomplete.
"""

from __future__ import annotations

import contextlib
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any, Optional

# ─────────────────────────────── constants ────────────────────────────────────
WINDOW_W, WINDOW_H = 460, 320
LOCK_DURATION = 30.0
TICK_INTERVAL = 0.1
APP_VERSION = "v2.0"
APP_ICON = Path(__file__).with_name("assets") / "app_icon.png"

BG_ROOT = "#0a0a0a"
BG_CARD = "#111111"
BG_BORDER = "#1e1e1e"

C_GREEN = "#00ff66"
C_GREEN_DIM = "#004d1f"
C_RED = "#ff3333"
C_RED_DIM = "#4d0000"
C_MUTED = "#444444"

F_TITLE = ("Courier New", 15, "bold")
F_SUBTITLE = ("Courier New", 9)
F_BIG = ("Courier New", 24, "bold")
F_SMALL = ("Courier New", 9)
F_BTN = ("Courier New", 11, "bold")
F_MICRO = ("Courier New", 8)


class HardwareSanitizerApp:
    """Neon-styled cleaner app with timed, global input suppression."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._active = False
        self._kbd: Optional[Any] = None
        self._mouse: Optional[Any] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._closing = False
        self._icon_image: Optional[tk.PhotoImage] = None

        self._setup_window()
        self._setup_styles()
        self._build_ui()

    # ── window ────────────────────────────────────────────────────────────────
    def _setup_window(self) -> None:
        self.root.title("Hardware Sanitizer Pro")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_ROOT)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._set_app_icon()

    def _set_app_icon(self) -> None:
        """Apply the bundled keyboard-cleaner icon when Tk supports PNG icons."""
        if not APP_ICON.exists():
            return

        with contextlib.suppress(tk.TclError):
            self._icon_image = tk.PhotoImage(file=str(APP_ICON))
            self.root.iconphoto(True, self._icon_image)

    # ── ttk styles ────────────────────────────────────────────────────────────
    def _setup_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        for name, bg, trough in (
            ("Green.Horizontal.TProgressbar", C_GREEN, "#001a0a"),
            ("Red.Horizontal.TProgressbar", C_RED, "#1a0000"),
        ):
            style.configure(
                name,
                troughcolor=trough,
                background=bg,
                bordercolor=BG_CARD,
                lightcolor=bg,
                darkcolor=bg,
                thickness=6,
            )

    # ── layout ────────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=BG_ROOT, padx=24, pady=16)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=BG_ROOT)
        header.pack(fill="x")

        tk.Label(
            header,
            text="⬡  HARDWARE SANITIZER PRO",
            font=F_TITLE,
            bg=BG_ROOT,
            fg=C_GREEN,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            header,
            text=APP_VERSION,
            font=F_MICRO,
            bg=BG_ROOT,
            fg=C_MUTED,
            anchor="e",
        ).pack(side="right", padx=(0, 2), pady=(8, 0))

        tk.Label(
            outer,
            text="Suppresses keyboard · mouse · trackpad · Bluetooth peripherals",
            font=F_SUBTITLE,
            bg=BG_ROOT,
            fg=C_GREEN_DIM,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        tk.Frame(outer, bg=C_MUTED, height=1).pack(fill="x", pady=(10, 0))

        self._card = tk.Frame(
            outer,
            bg=BG_CARD,
            highlightbackground=BG_BORDER,
            highlightthickness=1,
            padx=20,
            pady=12,
        )
        self._card.pack(fill="x", pady=(10, 0))

        status_row = tk.Frame(self._card, bg=BG_CARD)
        status_row.pack(fill="x")

        self._dot = tk.Label(
            status_row,
            text="●",
            font=("Courier New", 10),
            bg=BG_CARD,
            fg=C_GREEN,
        )
        self._dot.pack(side="left", padx=(0, 6))

        self._tag = tk.Label(
            status_row,
            text="STANDBY",
            font=F_SMALL,
            bg=BG_CARD,
            fg=C_MUTED,
        )
        self._tag.pack(side="left")

        self._big = tk.Label(
            self._card,
            text="READY",
            font=F_BIG,
            bg=BG_CARD,
            fg=C_GREEN,
        )
        self._big.pack(anchor="w", pady=(4, 0))

        self._desc = tk.Label(
            self._card,
            text="All input devices active",
            font=F_SUBTITLE,
            bg=BG_CARD,
            fg=C_GREEN_DIM,
        )
        self._desc.pack(anchor="w", pady=(2, 0))

        self._pb_var = tk.DoubleVar(value=100.0)
        self._pb = ttk.Progressbar(
            outer,
            orient="horizontal",
            mode="determinate",
            variable=self._pb_var,
            style="Red.Horizontal.TProgressbar",
        )

        self._bottom = tk.Frame(outer, bg=BG_ROOT)
        self._bottom.pack(fill="x", pady=(12, 0))

        badge_row = tk.Frame(self._bottom, bg=BG_ROOT)
        badge_row.pack(side="left", anchor="s")

        for label in ("USB", "BT", "RF", "HID"):
            tk.Label(
                badge_row,
                text=label,
                font=F_MICRO,
                bg="#1a1a1a",
                fg=C_MUTED,
                padx=5,
                pady=2,
            ).pack(side="left", padx=(0, 4))

        self._btn = tk.Button(
            self._bottom,
            text="▶  INITIATE CLEAN",
            font=F_BTN,
            bg=C_GREEN,
            fg="#000000",
            activebackground="#00cc55",
            activeforeground="#000000",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._on_start,
        )
        self._btn.pack(side="right")

        tk.Label(
            outer,
            text="Input suppression via pynput · OS message-stream intercept",
            font=F_MICRO,
            bg=BG_ROOT,
            fg="#252525",
        ).pack(side="bottom", anchor="w", pady=(6, 0))

    # ── progress bar show / hide ──────────────────────────────────────────────
    def _show_pb(self) -> None:
        self._pb_var.set(100.0)
        self._pb.pack(after=self._card, fill="x", pady=(8, 0))

    def _hide_pb(self) -> None:
        self._pb.pack_forget()
        self._pb_var.set(100.0)

    # ── idle / lock theme helpers ─────────────────────────────────────────────
    def _go_idle(self) -> None:
        self._dot.config(fg=C_GREEN)
        self._tag.config(text="STANDBY", fg=C_MUTED)
        self._big.config(text="READY", fg=C_GREEN)
        self._desc.config(text="All input devices active", fg=C_GREEN_DIM)
        self._btn.config(
            text="▶  INITIATE CLEAN",
            state="normal",
            bg=C_GREEN,
            fg="#000000",
        )
        self._hide_pb()

    def _go_lock(self) -> None:
        self._dot.config(fg=C_RED)
        self._tag.config(text="LOCKED", fg=C_RED)
        self._big.config(text=f"{LOCK_DURATION:.1f}s", fg=C_RED)
        self._desc.config(
            text="All peripherals suppressed — do not force-quit",
            fg=C_RED_DIM,
        )
        self._btn.config(
            text="■  LOCK ACTIVE",
            state="disabled",
            bg="#200000",
            fg=C_RED,
        )
        self._show_pb()

    def _go_error(self, message: str) -> None:
        self._dot.config(fg=C_RED)
        self._tag.config(text="ERROR", fg=C_RED)
        self._big.config(text="FAILED", fg=C_RED)
        self._desc.config(text=message, fg=C_RED_DIM)
        self._btn.config(
            text="▶  TRY AGAIN",
            state="normal",
            bg=C_GREEN,
            fg="#000000",
        )
        self._hide_pb()

    # ── pynput listeners ──────────────────────────────────────────────────────
    def _start_listeners(self) -> None:
        """Start suppressing keyboard and pointer HID events globally."""
        from pynput import keyboard, mouse

        self._kbd = keyboard.Listener(
            suppress=True,
            on_press=lambda key: None,
            on_release=lambda key: None,
        )
        self._mouse = mouse.Listener(
            suppress=True,
            on_move=lambda x, y: None,
            on_click=lambda x, y, button, pressed: None,
            on_scroll=lambda x, y, dx, dy: None,
        )
        self._kbd.start()
        self._mouse.start()

    def _stop_listeners(self) -> None:
        for listener in (self._kbd, self._mouse):
            if listener is not None:
                with contextlib.suppress(Exception):
                    listener.stop()
        self._kbd = None
        self._mouse = None

    # ── background worker thread ──────────────────────────────────────────────
    def _worker(self) -> None:
        """Count down in TICK_INTERVAL steps and push GUI updates via after()."""
        started_at = time.monotonic()

        while not self._stop_event.is_set():
            elapsed = time.monotonic() - started_at
            remaining = max(LOCK_DURATION - elapsed, 0.0)
            pct = (remaining / LOCK_DURATION) * 100.0
            self._schedule_ui(self._tick_ui, remaining, pct)

            if remaining <= 0.0:
                break

            time.sleep(TICK_INTERVAL)

        self._active = False
        self._stop_event.set()
        self._stop_listeners()

        if not self._closing:
            self._schedule_ui(self._on_lock_done)

    def _schedule_ui(self, callback: Any, *args: Any) -> None:
        """Safely schedule a Tk callback if the window still exists."""
        if self._closing:
            return
        with contextlib.suppress(tk.TclError, RuntimeError):
            self.root.after(0, callback, *args)

    def _tick_ui(self, remaining: float, pct: float) -> None:
        if not self._active:
            return
        self._big.config(text=f"{remaining:.1f}s")
        self._pb_var.set(pct)

    # ── event handlers ────────────────────────────────────────────────────────
    def _on_start(self) -> None:
        if self._active:
            return

        self._active = True
        self._stop_event.clear()
        self._go_lock()
        self.root.bell()

        try:
            self._start_listeners()
        except Exception as exc:
            self._active = False
            self._stop_event.set()
            self._stop_listeners()
            self._go_error("Grant input permissions or run with elevated privileges")
            messagebox.showerror(
                "Input suppression failed",
                "Hardware Sanitizer Pro could not start keyboard/mouse suppression.\n\n"
                "Grant the required OS permissions and try again.\n\n"
                f"Details: {exc}",
            )
            return

        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,
            name="SanitizerWorker",
        )
        self._thread.start()

    def _on_lock_done(self) -> None:
        self.root.bell()
        self._go_idle()

    def _on_close(self) -> None:
        self._closing = True
        if self._active:
            self._active = False
            self._stop_event.set()
            self._stop_listeners()
        self.root.destroy()


# ──────────────────────────────── entry point ─────────────────────────────────
def main() -> None:
    root = tk.Tk()
    HardwareSanitizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
