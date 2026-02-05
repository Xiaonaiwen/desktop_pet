"""
Movement system for Wanderer Mode.
Pet walks CLOCKWISE around the screen edges in a predictable pattern.
"""

import random
from typing import Tuple, Optional
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QApplication

import config


class MovementController:
    """Controls character movement in CLOCKWISE pattern around edges."""
    
    def __init__(self, window_width: int = 900, window_height: int = 900):
        """Initialize movement controller."""
        self.window_width = window_width
        self.window_height = window_height
        
        # Get screen dimensions
        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # Safe margins
        self.margin = 50
        
        # Edge thickness (how far from actual edge)
        self.edge_distance = 100  # Pet stays 100px from screen edge
        
        # Movement speed
        self.speed = 3
        
        # Current state
        self.current_pos = QPoint(0, 0)
        self.target_pos = None
        self.is_moving = False
        self.direction = "right"
        
        # Clockwise state: which edge are we currently on?
        # Order: BOTTOM → RIGHT → TOP → LEFT → BOTTOM
        self.current_edge = "BOTTOM"
        
        # Calculate corner positions
        self._calculate_corners()
    
    def _calculate_corners(self):
        """
        Calculate corners to place CHARACTER SPRITE (200x200 box) at screen corners.
        Window is 900x900, character sprite is 200x200 centered at (350, 350) offset.
        Window CAN go off-screen.
        """
        # Character sprite is 200x200, positioned at this offset in 900x900 window:
        sprite_offset_x = (self.window_width - 200) // 2  # (900 - 200) / 2 = 350
        sprite_offset_y = (self.window_height - 200) // 2  # 350
        
        # Sprite corners within the window:
        # Top-left of sprite: (350, 350)
        # Top-right of sprite: (550, 350)
        # Bottom-left of sprite: (350, 550)
        # Bottom-right of sprite: (550, 550)
        
        sprite_width = 200
        sprite_height = 200
        
        # To put sprite's BOTTOM-LEFT at screen (0, screen_height):
        # Sprite bottom-left is at (350, 550) in window coordinates
        # So window needs to be at: (0 - 350, screen_height - 550)
        self.bottom_left = QPoint(
            0 - sprite_offset_x,
            self.screen_height - (sprite_offset_y + sprite_height)
        )
        
        # To put sprite's BOTTOM-RIGHT at screen (screen_width, screen_height):
        # Sprite bottom-right is at (550, 550) in window coordinates
        # So window needs to be at: (screen_width - 550, screen_height - 550)
        self.bottom_right = QPoint(
            self.screen_width - (sprite_offset_x + sprite_width),
            self.screen_height - (sprite_offset_y + sprite_height)
        )
        
        # To put sprite's TOP-RIGHT at screen (screen_width, 0):
        # Sprite top-right is at (550, 350) in window coordinates
        # So window needs to be at: (screen_width - 550, 0 - 350)
        self.top_right = QPoint(
            self.screen_width - (sprite_offset_x + sprite_width),
            0 - sprite_offset_y
        )
        
        # To put sprite's TOP-LEFT at screen (0, 0):
        # Sprite top-left is at (350, 350) in window coordinates
        # So window needs to be at: (0 - 350, 0 - 350)
        self.top_left = QPoint(
            0 - sprite_offset_x,
            0 - sprite_offset_y
        )
        
        print(f"[movement] Screen: {self.screen_width}x{self.screen_height}")
        print(f"[movement] Window: {self.window_width}x{self.window_height}")
        print(f"[movement] Sprite: 200x200 at offset ({sprite_offset_x}, {sprite_offset_y})")
        print(f"[movement] Corner window positions (CAN go off-screen):")
        print(f"  Bottom-left:  ({self.bottom_left.x()}, {self.bottom_left.y()}) → sprite corner at (0, {self.screen_height})")
        print(f"  Bottom-right: ({self.bottom_right.x()}, {self.bottom_right.y()}) → sprite corner at ({self.screen_width}, {self.screen_height})")
        print(f"  Top-right:    ({self.top_right.x()}, {self.top_right.y()}) → sprite corner at ({self.screen_width}, 0)")
        print(f"  Top-left:     ({self.top_left.x()}, {self.top_left.y()}) → sprite corner at (0, 0)")
    
    def get_starting_position(self) -> QPoint:
        """Get the starting position (bottom-left corner)."""
        return QPoint(self.bottom_left.x(), self.bottom_left.y())
    
    def set_current_position(self, pos: QPoint):
        """Update current position."""
        self.current_pos = QPoint(pos.x(), pos.y())
        print(f"[movement] Position set to ({pos.x()}, {pos.y()})")
    
    def start_walking_to_next_corner(self) -> str:
        """
        Start walking to the next corner in clockwise direction.
        Returns the direction for animation (left or right).
        """
        # Determine next corner based on current edge
        if self.current_edge == "BOTTOM":
            # Bottom edge → going to bottom-right corner
            self.target_pos = QPoint(self.bottom_right.x(), self.bottom_right.y())
            self.current_edge = "RIGHT"
            self.direction = "right"
            print("[movement] Walking along BOTTOM edge → bottom-right corner")
        
        elif self.current_edge == "RIGHT":
            # Right edge → going to top-right corner
            self.target_pos = QPoint(self.top_right.x(), self.top_right.y())
            self.current_edge = "TOP"
            self.direction = "right"  # Still moving right visually
            print("[movement] Walking along RIGHT edge → top-right corner")
        
        elif self.current_edge == "TOP":
            # Top edge → going to top-left corner
            self.target_pos = QPoint(self.top_left.x(), self.top_left.y())
            self.current_edge = "LEFT"
            self.direction = "left"
            print("[movement] Walking along TOP edge → top-left corner")
        
        else:  # LEFT
            # Left edge → going to bottom-left corner
            self.target_pos = QPoint(self.bottom_left.x(), self.bottom_left.y())
            self.current_edge = "BOTTOM"
            self.direction = "left"  # Still moving left visually
            print("[movement] Walking along LEFT edge → bottom-left corner")
        
        self.is_moving = True
        return self.direction
    
    def update_position(self) -> Tuple[QPoint, bool, str]:
        """Update position towards target corner."""
        if not self.is_moving or self.target_pos is None:
            return self.current_pos, False, self.direction
        
        # Calculate vector to target
        dx = self.target_pos.x() - self.current_pos.x()
        dy = self.target_pos.y() - self.current_pos.y()
        
        # Calculate distance
        distance = (dx**2 + dy**2) ** 0.5
        
        # Check if reached target
        if distance < self.speed:
            self.current_pos = QPoint(self.target_pos.x(), self.target_pos.y())
            self.is_moving = False
            print(f"[movement] Reached corner at ({self.current_pos.x()}, {self.current_pos.y()})")
            return self.current_pos, True, self.direction
        
        # Move towards target
        move_x = int((dx / distance) * self.speed)
        move_y = int((dy / distance) * self.speed)
        
        self.current_pos = QPoint(
            self.current_pos.x() + move_x,
            self.current_pos.y() + move_y
        )
        
        return self.current_pos, False, self.direction
    
    def stop_moving(self):
        """Stop movement."""
        self.is_moving = False
        print("[movement] Stopped")
    
    def find_closest_edge_position(self, current_pos: QPoint) -> tuple[QPoint, str]:
        """
        Find the closest edge and calculate perpendicular return position.
        Returns (target_position, edge_name) tuple.
        
        The pet will return to a position ON the edge, perpendicular to where it was dragged from.
        """
        # Calculate sprite center in screen coordinates
        sprite_offset_x = (self.window_width - 200) // 2  # 350
        sprite_offset_y = (self.window_height - 200) // 2  # 350
        
        sprite_center_x = current_pos.x() + sprite_offset_x + 100  # +100 for sprite center
        sprite_center_y = current_pos.y() + sprite_offset_y + 100
        
        # Calculate distance to each edge
        dist_to_left = sprite_center_x
        dist_to_right = self.screen_width - sprite_center_x
        dist_to_top = sprite_center_y
        dist_to_bottom = self.screen_height - sprite_center_y
        
        # Find closest edge
        distances = {
            'LEFT': dist_to_left,
            'RIGHT': dist_to_right,
            'TOP': dist_to_top,
            'BOTTOM': dist_to_bottom
        }
        
        closest_edge = min(distances, key=distances.get)
        print(f"[movement] Closest edge: {closest_edge} (distance: {distances[closest_edge]}px)")
        
        # Calculate return position based on closest edge
        if closest_edge == 'LEFT':
            # Return to left edge, keep Y position
            target_screen_x = 0
            target_screen_y = sprite_center_y
            # Convert screen position to window position (sprite corner)
            target_pos = QPoint(
                target_screen_x - sprite_offset_x,
                target_screen_y - sprite_offset_y - 100
            )
        elif closest_edge == 'RIGHT':
            # Return to right edge, keep Y position
            target_screen_x = self.screen_width
            target_screen_y = sprite_center_y
            target_pos = QPoint(
                target_screen_x - sprite_offset_x - 200,
                target_screen_y - sprite_offset_y - 100
            )
        elif closest_edge == 'TOP':
            # Return to top edge, keep X position
            target_screen_x = sprite_center_x
            target_screen_y = 0
            target_pos = QPoint(
                target_screen_x - sprite_offset_x - 100,
                target_screen_y - sprite_offset_y
            )
        else:  # BOTTOM
            # Return to bottom edge, keep X position
            target_screen_x = sprite_center_x
            target_screen_y = self.screen_height
            target_pos = QPoint(
                target_screen_x - sprite_offset_x - 100,
                target_screen_y - sprite_offset_y - 200
            )
        
        print(f"[movement] Return position: ({target_pos.x()}, {target_pos.y()})")
        return target_pos, closest_edge
