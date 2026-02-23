# main.py
# ---------------------------------------------------------------------------
# Entry point for the Desktop Pet app.
# Creates the Qt application, loads the character, opens the window,
# starts the mode manager, and runs the event loop.
# 
# Phase 6: Added Interactive Mode with user-triggered actions (slap, hang, feed, pet).
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
        
        interactive_action = QAction("🎮 Interactive Mode", self.window)
        interactive_action.setToolTip("Manual control - trigger actions yourself")
        interactive_action.triggered.connect(lambda: self.mode_manager.switch_to_interactive())
        if current_mode == "interactive":
            interactive_action.setEnabled(False)  # Disable if already in this mode
        menu.addAction(interactive_action)
        
        # --- Separator ---
        menu.addSeparator()
        
        # --- Interactive actions (only show in Interactive Mode) ---
        if current_mode == "interactive":
            slap_action = QAction("👋 Slap", self.window)
            slap_action.setToolTip("Give them a playful slap")
            slap_action.triggered.connect(lambda: self.mode_manager.trigger_slap())
            menu.addAction(slap_action)
            
            # Check if currently floating (using persistent flag)
            is_floating = self.mode_manager._was_floating_before_action
            
            # Show ONLY Float or Unfloat (not both)
            if is_floating:
                # Currently floating - show only Unfloat
                unfloat_action = QAction("📤 Unfloat", self.window)
                unfloat_action.setToolTip("Return them to the ground")
                unfloat_action.triggered.connect(lambda: self.mode_manager.trigger_unfloat())
                menu.addAction(unfloat_action)
            else:
                # Not floating - show only Float
                float_action = QAction("🎈 Float", self.window)
                float_action.setToolTip("Make them levitate with magical energy")
                float_action.triggered.connect(lambda: self.mode_manager.trigger_float())
                menu.addAction(float_action)
            
            feed_action = QAction("🍪 Feed", self.window)
            feed_action.setToolTip("Give them a treat")
            feed_action.triggered.connect(lambda: self.mode_manager.trigger_feed())
            menu.addAction(feed_action)
            
            pet_action = QAction("💕 Pet", self.window)
            pet_action.setToolTip("Pet them affectionately")
            pet_action.triggered.connect(lambda: self.mode_manager.trigger_pet())
            menu.addAction(pet_action)
            
            # Separator before quit
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
