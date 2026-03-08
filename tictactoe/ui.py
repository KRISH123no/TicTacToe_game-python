# ui.py - UI elements and indicators

import pygame
from settings import *


class Button:
    """Button class for menu interactions"""
    
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False
        self.hover_animation = 0
    
    def handle_event(self, event):
        """Handle mouse click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False
    
    def update(self):
        """Update hover state"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Smooth hover animation
        target = 1.0 if self.is_hovered else 0.0
        self.hover_animation += (target - self.hover_animation) * 0.2
    
    def draw(self, surface):
        """Draw the button with hover effect"""
        # Draw button background with gradient effect based on hover
        base_color = COLOR_BUTTON
        hover_color = COLOR_BUTTON_HOVER
        
        r = int(base_color[0] + (hover_color[0] - base_color[0]) * self.hover_animation)
        g = int(base_color[1] + (hover_color[1] - base_color[1]) * self.hover_animation)
        b = int(base_color[2] + (hover_color[2] - base_color[2]) * self.hover_animation)
        
        # Draw rounded rectangle
        pygame.draw.rect(surface, (r, g, b), self.rect, border_radius=12)
        
        # Draw amber gold border
        border_width = 3 + int(2 * self.hover_animation)
        pygame.draw.rect(surface, COLOR_ACCENT, self.rect, border_width, border_radius=12)
        
        # Draw text
        text_surface = FONT_BUTTON.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ToggleButton:
    """Toggle button for settings"""
    
    def __init__(self, x, y, width, height, text, is_active=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_active = is_active
    
    def handle_event(self, event):
        """Handle click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_active = not self.is_active
                return True
        return False
    
    def draw(self, surface):
        """Draw toggle button"""
        # Background
        bg_color = COLOR_ACCENT if self.is_active else COLOR_BUTTON
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        
        # Border
        border_color = COLOR_TEXT if self.is_active else COLOR_ACCENT
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=8)
        
        # Text
        text_surface = FONT_BUTTON.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class ScoreTracker:
    """Displays score during gameplay"""
    
    def __init__(self):
        self.score_x = 0
        self.score_o = 0
        self.draws = 0
    
    def reset(self):
        """Reset scores"""
        self.score_x = 0
        self.score_o = 0
        self.draws = 0
    
    def add_win(self, winner):
        """Add a win for the winner"""
        if winner == 'X':
            self.score_x += 1
        elif winner == 'O':
            self.score_o += 1
        else:
            self.draws += 1
    
    def draw(self, surface, game_mode):
        """Draw score display"""
        if game_mode == "ai":
            label_x = "Player X:"
            label_o = "Bot:"
        else:
            label_x = "Player 1:"
            label_o = "Player 2:"
        
        score_text = f"{label_x} {self.score_x}   |   Draws: {self.draws}   |   {label_o} {self.score_o}"
        
        text_surface = FONT_SCORE.render(score_text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
        surface.blit(text_surface, text_rect)


def draw_text_centered(surface, text, font, color, center_x, center_y):
    """Draw text centered at position"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)


def drawWoodenFrame(surface, rect, border_width=8):
    """Draw a wooden frame effect around a rectangle"""
    # Outer darker border
    pygame.draw.rect(surface, (40, 20, 10), rect, border_width + 4, border_radius=8)
    # Inner amber accent
    pygame.draw.rect(surface, COLOR_GRID, rect, border_width, border_radius=8)


def drawWoodenBackground(surface):
    """Draw wooden texture background"""
    # Base background
    surface.fill(COLOR_BACKGROUND)
    
    # Add subtle wood grain effect with horizontal lines
    for y in range(0, WINDOW_HEIGHT, 30):
        alpha = 15 if y % 60 == 0 else 8
        pygame.draw.line(surface, (90, 50, 35), (0, y), (WINDOW_WIDTH, y), 1)
    
    # Add some wood knots/grains
    pygame.draw.circle(surface, (90, 50, 35), (100, 200), 40, 1)
    pygame.draw.circle(surface, (80, 45, 30), (700, 500), 30, 1)
    pygame.draw.circle(surface, (85, 48, 32), (600, 150), 25, 1)
