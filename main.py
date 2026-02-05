# main.py
# ---------------------------------------------------------------------------
# Entry point for the Desktop Pet app.
# Creates the Qt application, loads the character, opens the window,
# starts the mode manager, and runs the event loop.
# ---------------------------------------------------------------------------

import sys
from PyQt6.QtWidgets import QApplication

from character import Character
from window_manager import PetWindow
from mode_manager import ModeManager


def main():
    # 1. Create the Qt application (required before any QWidget)
    app = QApplication(sys.argv)

    # 2. Load the character (sprite or placeholder)
    character = Character()

    # 3. Create and show the pet window
    window = PetWindow(character)
    window.show()

    # 4. Start the mode manager — this kicks off Supervisor mode automatically
    mode_manager = ModeManager(character, window)

    # 5. Enter the Qt event loop — this keeps the app running
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
