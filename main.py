# main.py
# ---------------------------------------------------------------------------
# Entry point for the Desktop Pet app.
# Creates the Qt application, loads the character, opens the window, and runs.
# ---------------------------------------------------------------------------

import sys
from PyQt6.QtWidgets import QApplication

from character import Character
from window_manager import PetWindow


def main():
    # 1. Create the Qt application (required before any QWidget)
    app = QApplication(sys.argv)

    # 2. Load the character (sprite or placeholder)
    character = Character()

    # 3. Create and show the pet window
    window = PetWindow(character)
    window.show()

    # 4. Enter the Qt event loop — this keeps the app running
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
