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
        """Start walking to next corner in clockwise pattern."""
        direction = self.movement.start_walking_to_next_corner()
        
        # Set walk animation
        if direction == "left":
            self.character.set_animation("walk_left")
        else:
            self.character.set_animation("walk_right")

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
        
        # Determine direction for sad walk animation based on target
        dx = return_target.x() - new_pos.x()
        if dx > 0:
            self.character.set_animation("sad_walk_right")
            print(f"[wanderer] Walking sadly RIGHT to {closest_edge} edge")
        else:
            self.character.set_animation("sad_walk_left")
            print(f"[wanderer] Walking sadly LEFT to {closest_edge} edge")
        
        print(f"[wanderer] Target position: ({return_target.x()}, {return_target.y()})")
