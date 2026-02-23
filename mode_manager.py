# mode_manager.py
# Wanderer Mode: Pet walks clockwise around screen edges with random poses

import random
from PyQt6.QtCore import QTimer, QPoint

import config
from character import Character
from window_manager import PetWindow
from app_monitor import AppMonitor
from movement import MovementController


class ModeManager:
    """Manages Supervisor and Wanderer modes."""

    def __init__(self, character: Character, window: PetWindow):
        self.character = character
        self.window = window
        
        # --- Supervisor Mode components ---
        self.app_monitor = AppMonitor()
        self._check_timer = QTimer()
        self._check_timer.setInterval(config.APP_CHECK_INTERVAL_MS)
        self._check_timer.timeout.connect(self._on_supervisor_tick)
        self._bubble_timer = QTimer()
        self._bubble_timer.setInterval(config.SPEECH_BUBBLE_DURATION_MS)
        self._bubble_timer.timeout.connect(self._hide_bubble)

        # --- Wanderer Mode components ---
        self.movement = MovementController(window_width=900, window_height=900)
        self._movement_timer = QTimer()
        self._movement_timer.setInterval(config.MOVEMENT_UPDATE_INTERVAL_MS)
        self._movement_timer.timeout.connect(self._on_wanderer_movement_tick)
        self._pose_timer = QTimer()
        self._pose_timer.timeout.connect(self._on_pose_done)
        
        # --- Wanderer state tracking ---
        self._wanderer_state = "idle"  # idle, walking, posing, returning_to_edge, touching_ears, being_dragged
        self._previous_wanderer_state = None  # Store state before drag
        self._return_target = None
        self._return_edge = None

        # --- Interactive Mode components ---
        self._interactive_state = "idle"  # idle, slapping, floating, eating, petting, satisfied
        self._float_timer = QTimer()
        self._float_timer.timeout.connect(self._on_float_toggle)
        self._float_phase = "active"  # active or calm
        self._was_floating_before_action = False  # Track if action was done while floating
        
        self._action_timer = QTimer()  # For timed actions (slap, feed, pet)
        self._action_timer.timeout.connect(self._on_action_complete)

        # --- Current mode ---
        self.current_mode = None

        # Start in Supervisor mode
        self.switch_to_supervisor()

    # ========================================================================
    # Mode Switching
    # ========================================================================

    def switch_to_supervisor(self):
        """Switch to Supervisor mode."""
        if self.current_mode == "supervisor":
            return
        
        print("[mode_manager] Switching to Supervisor mode")
        
        # Stop wanderer
        self._movement_timer.stop()
        self._pose_timer.stop()
        self.movement.stop_moving()
        
        # Start supervisor
        self.current_mode = "supervisor"
        self._hide_bubble()
        self.character.set_animation("idle")
        self._check_timer.start()

    def switch_to_wanderer(self):
        """Switch to Wanderer mode - starts at bottom-left, walks clockwise."""
        if self.current_mode == "wanderer":
            return
        
        print("[mode_manager] Switching to Wanderer mode")
        
        # Stop supervisor
        self._check_timer.stop()
        self._bubble_timer.stop()
        
        # Stop interactive (IMPORTANT - was missing!)
        self._float_timer.stop()
        self._action_timer.stop()
        
        # Set mode and reset state
        self.current_mode = "wanderer"
        self._wanderer_state = "idle"
        self._previous_wanderer_state = None
        self._return_target = None
        self._return_edge = None
        self._hide_bubble()
        
        # Move to starting position (bottom-left)
        starting_pos = self.movement.get_starting_position()
        print(f"[wanderer] Moving to starting position: ({starting_pos.x()}, {starting_pos.y()})")
        self.window.move(starting_pos)
        self.movement.set_current_position(starting_pos)
        
        # RESET movement controller state (CRITICAL FIX)
        self.movement.is_moving = False
        self.movement.target_pos = None
        self.movement.current_edge = "BOTTOM"  # Start from bottom edge
        
        # Start walking after brief idle
        self.character.set_animation("idle")
        self._pose_timer.setSingleShot(True)
        self._pose_timer.start(2000)  # 2 second idle before starting
        
        # Start movement updates
        self._movement_timer.start()

    # ========================================================================
    # Supervisor Mode
    # ========================================================================

    def _on_supervisor_tick(self):
        """Check active app and trigger reaction."""
        reaction = self.app_monitor.check()
        if reaction is None:
            return

        animation_name, speech_text = reaction
        self.character.set_animation(animation_name)

        if speech_text:
            self.window.show_speech_bubble(speech_text)
            self._bubble_timer.start()
        else:
            self._hide_bubble()

    def _hide_bubble(self):
        """Hide speech bubble."""
        self._bubble_timer.stop()
        self.window.hide_speech_bubble()
        if self.current_mode == "supervisor":
            self.character.set_animation("idle")

    # ========================================================================
    # Wanderer Mode - Clockwise Movement
    # ========================================================================

    def _on_wanderer_movement_tick(self):
        """Update position during walking."""
        if self._wanderer_state == "being_dragged":
            # Don't update position while user is dragging
            # The window_manager handles position updates during drag
            return
        
        if self._wanderer_state == "returning_to_edge":
            # Returning to edge after being dragged
            new_pos, reached_target, direction = self._update_return_to_edge()
            self.window.move(new_pos)
            
            if reached_target:
                print("[wanderer] Reached edge! Touching ears sadly...")
                self._wanderer_state = "touching_ears"
                self.character.set_animation("touching_ears_sad")
                
                # Update movement controller's position to the edge position
                self.movement.set_current_position(new_pos)
                
                # After touching ears, resume normal wanderer behavior
                self._pose_timer.setSingleShot(True)
                self._pose_timer.start(2000)  # 2 seconds of ear touching
        
        elif self._wanderer_state == "walking":
            # Normal clockwise walking
            new_pos, reached_corner, direction = self.movement.update_position()
            self.window.move(new_pos)
            
            if reached_corner:
                print("[wanderer] Reached corner!")
                self._wanderer_state = "posing"
                self._do_random_pose()
    
    def _update_return_to_edge(self) -> tuple:
        """Update position while returning to edge after drag."""
        current_pos = self.window.pos()
        
        # Calculate vector to target
        dx = self._return_target.x() - current_pos.x()
        dy = self._return_target.y() - current_pos.y()
        distance = (dx**2 + dy**2) ** 0.5
        
        # Determine direction for animation
        direction = "right" if dx > 0 else "left"
        
        # Check if reached
        if distance < self.movement.speed:
            return self._return_target, True, direction
        
        # Move towards target
        move_x = int((dx / distance) * self.movement.speed)
        move_y = int((dy / distance) * self.movement.speed)
        new_pos = QPoint(current_pos.x() + move_x, current_pos.y() + move_y)
        
        return new_pos, False, direction

    def _on_pose_done(self):
        """Called when pose duration ends - start walking to next corner OR resume after touching ears."""
        if self._wanderer_state == "touching_ears":
            # After touching ears sadly, resume normal wanderer behavior
            # Simply continue to the next corner in clockwise order based on which edge we're on
            print(f"[wanderer] Resuming clockwise cycle from {self._return_edge} edge")
            
            # Set current_edge to the edge we returned to
            # start_walking_to_next_corner will then go to the correct next corner
            self.movement.current_edge = self._return_edge
            
            # Update movement controller position
            self.movement.set_current_position(self.window.pos())
            
            self._wanderer_state = "walking"
            self._on_wanderer_start_next_walk()
            
        elif self._wanderer_state in ("posing", "idle"):
            # Normal pose ended OR initial idle ended, continue walking
            print("[wanderer] Starting walk to next corner")
            self._wanderer_state = "walking"
            self._on_wanderer_start_next_walk()
    
    def _on_wanderer_start_next_walk(self):
        """Start driving to next corner in clockwise pattern."""
        direction = self.movement.start_walking_to_next_corner()
        
        # Set driving animation
        if direction == "left":
            self.character.set_animation("driving_left")
        else:
            self.character.set_animation("driving_right")

    def _do_random_pose(self):
        """Show random pose at corner."""
        # Pick random pose
        pose = random.choice(config.WANDERER_POSES)
        print(f"[wanderer] Doing pose: {pose}")
        
        # Show pose
        self.character.set_animation(pose)
        self._wanderer_state = "posing"
        
        # Set duration
        duration = random.randint(
            config.MIN_POSE_DURATION * 1000,
            config.MAX_POSE_DURATION * 1000
        )
        
        # After pose, continue walking
        self._pose_timer.setSingleShot(True)
        self._pose_timer.start(duration)

    def on_pet_drag_start(self):
        """Handle drag start - show dragged_by_ear animation and pause wanderer."""
        if self.current_mode == "wanderer":
            print("[wanderer] Pet is being dragged by ear!")
            # Stop wanderer movement updates while being dragged
            # This prevents movement tick from interfering with drag
            self._previous_wanderer_state = self._wanderer_state
            self._wanderer_state = "being_dragged"
            self.movement.stop_moving()
            self._pose_timer.stop()
            # Show dragged animation (will stay on this until release)
            self.character.set_animation("dragged_by_ear")
    
    def on_pet_dragged(self, new_pos):
        """Handle drag END (mouse release) - pet returns to closest edge with sad animation."""
        if self.current_mode != "wanderer":
            return
        
        print(f"[wanderer] Pet released at ({new_pos.x()}, {new_pos.y()})")
        
        # Update current position to where the user dropped it
        self.movement.set_current_position(new_pos)
        
        # Find closest edge and calculate return position
        return_target, closest_edge = self.movement.find_closest_edge_position(new_pos)
        self._return_target = return_target
        self._return_edge = closest_edge
        
        # Start returning to edge with sad animation
        self._wanderer_state = "returning_to_edge"
        
        # Determine direction for sad driving animation based on target
        dx = return_target.x() - new_pos.x()
        if dx > 0:
            self.character.set_animation("driving_sad_right")
            print(f"[wanderer] Driving sadly RIGHT to {closest_edge} edge")
        else:
            self.character.set_animation("driving_sad_left")
            print(f"[wanderer] Driving sadly LEFT to {closest_edge} edge")
        
        print(f"[wanderer] Target position: ({return_target.x()}, {return_target.y()})")

    # ========================================================================
    # Interactive Mode - User-Triggered Actions
    # ========================================================================
    
    def switch_to_interactive(self):
        """Switch to Interactive mode - manual control."""
        if self.current_mode == "interactive":
            return
        
        print("[mode_manager] Switching to Interactive mode")
        
        # Stop supervisor
        self._check_timer.stop()
        self._bubble_timer.stop()
        
        # Stop wanderer
        self._movement_timer.stop()
        self._pose_timer.stop()
        self.movement.stop_moving()
        
        # Stop any interactive actions
        self._float_timer.stop()
        self._action_timer.stop()
        
        # Set mode and reset state
        self.current_mode = "interactive"
        self._interactive_state = "idle"
        self._hide_bubble()
        
        # Return to idle at current position
        self.character.set_animation("idle")
        
        print("[interactive] Ready for interactions! Right-click to choose action.")
    
    def trigger_slap(self):
        """User clicked 'Slap' - show reaction animation."""
        if self.current_mode != "interactive":
            return
        
        print("[interactive] *SLAP!* 👋")
        
        # Stop any ongoing actions
        self._float_timer.stop()
        self._action_timer.stop()
        
        # Check if currently floating OR if we were floating before a previous action
        # This handles rapid slapping while floating
        was_floating = (self._interactive_state == "floating" or 
                      (hasattr(self, '_was_floating_before_action') and self._was_floating_before_action))
        
        self._interactive_state = "slapping"
        
        # Show slap reaction (different animation if floating)
        if was_floating:
            self.character.set_animation("float_slap_reaction")
            self.window.show_speech_bubble("OW! 😵 (still floating!)")
        else:
            self.character.set_animation("slap_reaction")
            self.window.show_speech_bubble("OW! 😵 Why?!")
        
        # Return to previous state after animation
        self._action_timer.setSingleShot(True)
        self._action_timer.start(config.SLAP_REACTION_DURATION_MS)
        
        # Remember if we were floating before
        self._was_floating_before_action = was_floating
    
    def trigger_float(self):
        """User clicked 'Float' - character levitates with magical sparkly aura."""
        if self.current_mode != "interactive":
            return
        
        print("[interactive] Floating! 🎈")
        
        # Stop any ongoing actions
        self._float_timer.stop()
        self._action_timer.stop()
        
        self._interactive_state = "floating"
        self._float_phase = "active"
        
        # Set the floating flag so other actions know we're floating
        self._was_floating_before_action = True
        
        # Hide any speech bubble
        self.window.hide_speech_bubble()
        
        # Show floating animation
        self.character.set_animation("float_active")
        
        # After a while, switch to calm floating
        self._float_timer.setSingleShot(True)
        self._float_timer.start(config.FLOAT_ACTIVE_DURATION_MS)
    
    def trigger_unfloat(self):
        """User clicked 'Unfloat' - release from floating, return to idle."""
        if self.current_mode != "interactive":
            return
        
        print("[interactive] Back to ground! 😮‍💨")
        
        # Stop floating
        self._float_timer.stop()
        self._interactive_state = "idle"
        
        # Clear the floating flag so future actions know we're not floating anymore
        self._was_floating_before_action = False
        
        # Return to idle animation
        self.character.set_animation("idle")
        
        # Show relief message
        self.window.show_speech_bubble("Finally! 😅")
        
        # Hide bubble after a moment
        self._action_timer.setSingleShot(True)
        self._action_timer.start(2000)
    
    def _on_float_toggle(self):
        """Toggle between active and calm floating."""
        if self._interactive_state != "floating":
            return
        
        if self._float_phase == "active":
            self._float_phase = "calm"
            self.character.set_animation("float_calm")
            print("[interactive] Now floating calmly... 😌")
            
            # Alternate back to active after a while
            self._float_timer.setSingleShot(True)
            self._float_timer.start(config.FLOAT_CALM_DURATION_MS)
        else:
            self._float_phase = "active"
            self.character.set_animation("float_active")
            print("[interactive] Floating actively again! ✨")
            
            self._float_timer.setSingleShot(True)
            self._float_timer.start(config.FLOAT_ACTIVE_DURATION_MS)
    
    def trigger_feed(self):
        """User clicked 'Feed' - eating animation."""
        if self.current_mode != "interactive":
            return
        
        print("[interactive] *nom nom nom* 🍪")
        
        # Stop any ongoing actions
        self._float_timer.stop()
        self._action_timer.stop()
        
        # Check if currently floating OR if we were floating before a previous action
        was_floating = (self._interactive_state == "floating" or 
                      (hasattr(self, '_was_floating_before_action') and self._was_floating_before_action))
        
        self._interactive_state = "eating"
        
        # Show eating animation (different if floating)
        if was_floating:
            self.character.set_animation("float_eating")
            self.window.show_speech_bubble("Yum! 😋 (still floating!)")
        else:
            self.character.set_animation("eating")
            self.window.show_speech_bubble("Yum! 😋")
        
        # After eating, show satisfied
        self._action_timer.setSingleShot(True)
        self._action_timer.start(config.EATING_DURATION_MS)
        
        # Remember if we were floating before
        self._was_floating_before_action = was_floating
    
    def trigger_pet(self):
        """User clicked 'Pet' - happy affection response."""
        if self.current_mode != "interactive":
            return
        
        print("[interactive] *pat pat* 💕")
        
        # Stop any ongoing actions
        self._float_timer.stop()
        self._action_timer.stop()
        
        # Check if currently floating OR if we were floating before a previous action
        was_floating = (self._interactive_state == "floating" or 
                      (hasattr(self, '_was_floating_before_action') and self._was_floating_before_action))
        
        self._interactive_state = "petting"
        
        # Show happy petting animation (different if floating)
        if was_floating:
            self.character.set_animation("float_petting_happy")
            self.window.show_speech_bubble("Hehe~ 💖 (still floating!)")
        else:
            self.character.set_animation("petting_happy")
            self.window.show_speech_bubble("Hehe~ 💖")
        
        # Return to previous state after animation
        self._action_timer.setSingleShot(True)
        self._action_timer.start(config.PETTING_DURATION_MS)
        
        # Remember if we were floating before
        self._was_floating_before_action = was_floating
    
    def _on_action_complete(self):
        """Called when a timed action finishes."""
        if self._interactive_state == "slapping":
            # Slap reaction done, return to previous state
            if hasattr(self, '_was_floating_before_action') and self._was_floating_before_action:
                # Return to floating
                self._interactive_state = "floating"
                self._float_phase = "calm"
                self.window.hide_speech_bubble()
                self.character.set_animation("float_calm")
                print("[interactive] Recovered from slap, back to floating")
                # Resume float alternation
                self._float_timer.setSingleShot(True)
                self._float_timer.start(config.FLOAT_CALM_DURATION_MS)
            else:
                # Return to idle
                self._interactive_state = "idle"
                self.window.hide_speech_bubble()
                self.character.set_animation("idle")
                print("[interactive] Recovered from slap, back to idle")
        
        elif self._interactive_state == "eating":
            # Eating done, show satisfied, then return to previous state
            self._interactive_state = "satisfied"
            
            # Use float version if was floating
            if hasattr(self, '_was_floating_before_action') and self._was_floating_before_action:
                self.character.set_animation("float_eating_satisfied")
                self.window.show_speech_bubble("So good! 😊 (still floating!)")
            else:
                self.character.set_animation("eating_satisfied")
                self.window.show_speech_bubble("So good! 😊")
            
            # After showing satisfaction, return to previous state
            self._action_timer.setSingleShot(True)
            self._action_timer.start(config.SATISFIED_DURATION_MS)
        
        elif self._interactive_state == "satisfied":
            # Satisfied done, return to previous state
            if hasattr(self, '_was_floating_before_action') and self._was_floating_before_action:
                # Return to floating
                self._interactive_state = "floating"
                self._float_phase = "calm"
                self.window.hide_speech_bubble()
                self.character.set_animation("float_calm")
                print("[interactive] Full and happy, back to floating")
                # Resume float alternation
                self._float_timer.setSingleShot(True)
                self._float_timer.start(config.FLOAT_CALM_DURATION_MS)
            else:
                # Return to idle
                self._interactive_state = "idle"
                self.window.hide_speech_bubble()
                self.character.set_animation("idle")
                print("[interactive] Full and happy, back to idle")
        
        elif self._interactive_state == "petting":
            # Petting done, return to previous state
            if hasattr(self, '_was_floating_before_action') and self._was_floating_before_action:
                # Return to floating
                self._interactive_state = "floating"
                self._float_phase = "calm"
                self.window.hide_speech_bubble()
                self.character.set_animation("float_calm")
                print("[interactive] That felt nice! Back to floating")
                # Resume float alternation
                self._float_timer.setSingleShot(True)
                self._float_timer.start(config.FLOAT_CALM_DURATION_MS)
            else:
                # Return to idle
                self._interactive_state = "idle"
                self.window.hide_speech_bubble()
                self.character.set_animation("idle")
                print("[interactive] That felt nice! Back to idle")
        
        elif self._interactive_state == "idle":
            # This handles the unfloat message timeout
            self.window.hide_speech_bubble()

