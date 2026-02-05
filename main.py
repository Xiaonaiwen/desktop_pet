# main.py
# ---------------------------------------------------------------------------
# Entry point for the Desktop Pet app.
# Creates the Qt application, loads the character, opens the window,
# starts the mode manager, and runs the event loop.
# 
# Phase 5: Added right-click context menu for switching between modes.
# ---------------------------------------------------------------------------

import sys
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from character import Character
from window_manager import PetWindow
from mode_manager import ModeManager


class DesktopPetApp:
    """Main application controller with mode switching."""
    
    def __init__(self):
        # 1. Create the Qt application (required before any QWidget)
        self.app = QApplication(sys.argv)
        
        # 2. Load the character (sprite or placeholder)
        self.character = Character()
        
        # 3. Create the pet window
        self.window = PetWindow(self.character)
        
        # 4. Create the mode manager
        self.mode_manager = ModeManager(self.character, self.window)
        
        # 5. Connect drag callbacks so mode_manager knows when pet is manually moved
        self.window.on_drag_start = self.mode_manager.on_pet_drag_start
        self.window.on_dragged = self.mode_manager.on_pet_dragged
        
        # 6. Setup right-click context menu
        self.window.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.window.customContextMenuRequested.connect(self._show_context_menu)
        
        # 7. Show the window
        self.window.show()
        
        print("[main] Desktop Pet started!")
        print("[main] Right-click the character to switch modes")
    
    def _show_context_menu(self, pos):
        """Show context menu when user right-clicks."""
        menu = QMenu(self.window)
        
        # Get current mode to disable its menu item
        current_mode = self.mode_manager.current_mode
        
        # --- Mode switching options ---
        supervisor_action = QAction("📊 Supervisor Mode", self.window)
        supervisor_action.setToolTip("Watch what apps you're using and react")
        supervisor_action.triggered.connect(lambda: self.mode_manager.switch_to_supervisor())
        if current_mode == "supervisor":
            supervisor_action.setEnabled(False)  # Disable if already in this mode
        menu.addAction(supervisor_action)
        
        wanderer_action = QAction("🚶 Wanderer Mode", self.window)
        wanderer_action.setToolTip("Walk around randomly and strike poses")
        wanderer_action.triggered.connect(lambda: self.mode_manager.switch_to_wanderer())
        if current_mode == "wanderer":
            wanderer_action.setEnabled(False)  # Disable if already in this mode
        menu.addAction(wanderer_action)
        
        # --- Separator ---
        menu.addSeparator()
        
        # --- Quit option ---
        quit_action = QAction("❌ Quit", self.window)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)
        
        # Show the menu at the cursor position
        menu.exec(self.window.mapToGlobal(pos))
    
    def run(self):
        """Run the Qt event loop."""
        return self.app.exec()


def main():
    app = DesktopPetApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
