# app_monitor.py
# ---------------------------------------------------------------------------
# Detects what application is currently active, cross-platform.
# Windows: uses pywin32 (win32gui) to get the focused window title
# Mac:     uses AppKit (NSWorkspace) to get the active app name
# ---------------------------------------------------------------------------

import sys
import config


class AppMonitor:
    """Polls the active window and returns the matching reaction."""

    def __init__(self):
        self._last_title = ""
        self._last_reaction = None

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------
    def check(self) -> tuple | None:
        """
        Check the currently active window.
        Returns (animation_name, speech_text) if the app changed, else None.
        """
        title = self._get_active_window_title()

        if title == self._last_title:
            return None

        self._last_title = title
        reaction = self._match_reaction(title)
        self._last_reaction = reaction

        if reaction:
            print(f"[app_monitor] Active window: '{title}' → reaction: {reaction[0]}")
        else:
            print(f"[app_monitor] Active window: '{title}' → no match")

        return reaction

    # ------------------------------------------------------------------
    # Internal — platform-specific window detection
    # ------------------------------------------------------------------
    def _get_active_window_title(self) -> str:
        """Get the active window title, dispatches to platform-specific method."""
        if sys.platform == "win32":
            return self._get_title_windows()
        elif sys.platform == "darwin":
            return self._get_title_mac()
        return ""

    def _get_title_windows(self) -> str:
        """Windows: use win32gui to get focused window title."""
        try:
            import win32gui
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return ""
            return win32gui.GetWindowText(hwnd)
        except Exception:
            return ""

    def _get_title_mac(self) -> str:
        """Mac: use AppKit NSWorkspace to get active application name."""
        try:
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            return active_app.get("NSApplicationName", "")
        except Exception:
            return ""

    # ------------------------------------------------------------------
    # Internal — reaction matching
    # ------------------------------------------------------------------
    def _match_reaction(self, title: str) -> tuple | None:
        """
        Compare the window title against APP_REACTIONS in config.
        Case-insensitive. First match wins.
        Returns (animation_name, speech_text) or None.
        """
        title_lower = title.lower()

        for keyword, animation, speech in config.APP_REACTIONS:
            if keyword.lower() in title_lower:
                return (animation, speech)

        return ("idle", None)
