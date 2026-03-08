# menu.py - Main menu and navigation

import pygame
from settings import *
from ui import Button, ToggleButton, drawWoodenBackground, draw_text_centered


class Menu:
    """Main menu screen"""
    
    def __init__(self):
        self.buttons = []
        self.settings_button = None
        self._create_buttons()
    
    def _create_buttons(self):
        """Create menu buttons"""
        button_width = 250
        button_height = 70
        center_x = WINDOW_WIDTH // 2
        
        # Multiplayer button
        multiplayer_y = WINDOW_HEIGHT // 2 - 50
        self.buttons.append(Button(
            center_x - button_width // 2,
            multiplayer_y,
            button_width,
            button_height,
            "Multiplayer",
            None
        ))
        
        # vs Bot button
        bot_y = multiplayer_y + 100
        self.buttons.append(Button(
            center_x - button_width // 2,
            bot_y,
            button_width,
            button_height,
            "vs Bot",
            None
        ))
        
        # Settings button (gear icon in top right)
        self.settings_button = Button(
            WINDOW_WIDTH - 60,
            20,
            40,
            40,
            "⚙",
            None
        )
    
    def handle_event(self, event):
        """Handle menu events"""
        for button in self.buttons:
            button.handle_event(event)
        
        self.settings_button.handle_event(event)
    
    def update(self):
        """Update menu state"""
        for button in self.buttons:
            button.update()
        self.settings_button.update()
    
    def draw(self, surface):
        """Draw the menu"""
        # Draw wooden background
        drawWoodenBackground(surface)
        
        # Draw title
        title_surface = FONT_TITLE.render("Tic Tac Toe", True, COLOR_TEXT)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = FONT_SUBTITLE.render("Choose a Mode", True, COLOR_TEXT)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 180))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
        
        # Draw settings button
        self.settings_button.draw(surface)
    
    def get_clicked_button(self, pos):
        """Check which button was clicked"""
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(pos):
                if i == 0:
                    return "multiplayer"
                elif i == 1:
                    return "ai"
        return None
    
    def is_settings_clicked(self, pos):
        """Check if settings button was clicked"""
        return self.settings_button.rect.collidepoint(pos)


class SettingsMenu:
    """Settings menu screen"""
    
    def __init__(self, first_player):
        self.back_button = None
        self.player_x_button = None
        self.player_o_button = None
        self.first_player = first_player
        self._create_buttons()
    
    def _create_buttons(self):
        """Create settings buttons"""
        button_width = 200
        button_height = 60
        center_x = WINDOW_WIDTH // 2
        
        # Back button
        self.back_button = Button(
            center_x - button_width // 2,
            WINDOW_HEIGHT - 120,
            button_width,
            button_height,
            "Back",
            None
        )
        
        # Player X first toggle
        self.player_x_button = ToggleButton(
            center_x - button_width // 2 - 120,
            WINDOW_HEIGHT // 2 - 30,
            button_width,
            button_height,
            "Player X",
            self.first_player == 'X'
        )
        
        # Player O first toggle
        self.player_o_button = ToggleButton(
            center_x - button_width // 2 + 120,
            WINDOW_HEIGHT // 2 - 30,
            button_width,
            button_height,
            "Player O",
            self.first_player == 'O'
        )
    
    def set_first_player(self, player):
        """Set who goes first"""
        self.first_player = player
        self.player_x_button.is_active = (player == 'X')
        self.player_o_button.is_active = (player == 'O')
    
    def handle_event(self, event):
        """Handle settings events"""
        self.back_button.handle_event(event)
        
        if self.player_x_button.handle_event(event):
            self.set_first_player('X')
        elif self.player_o_button.handle_event(event):
            self.set_first_player('O')
    
    def update(self):
        """Update settings state"""
        self.back_button.update()
    
    def draw(self, surface):
        """Draw settings menu"""
        # Draw wooden background
        drawWoodenBackground(surface)
        
        # Draw title
        title_surface = FONT_TITLE.render("Settings", True, COLOR_TEXT)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        surface.blit(title_surface, title_rect)
        
        # Draw who goes first label
        label_surface = FONT_SUBTITLE.render("Who goes first?", True, COLOR_TEXT)
        label_rect = label_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        surface.blit(label_surface, label_rect)
        
        # Draw toggle buttons
        self.player_x_button.draw(surface)
        self.player_o_button.draw(surface)
        
        # Draw back button
        self.back_button.draw(surface)
    
    def is_back_clicked(self, pos):
        """Check if back button was clicked"""
        return self.back_button.rect.collidepoint(pos)


class GameOverScreen:
    """Game over overlay screen"""
    
    def __init__(self):
        self.play_again_button = None
        self.main_menu_button = None
        self.winner = None
        self.game_mode = None
        self._create_buttons()
    
    def _create_buttons(self):
        """Create game over buttons"""
        button_width = 220
        button_height = 60
        center_x = WINDOW_WIDTH // 2
        
        # Play again button
        self.play_again_button = Button(
            center_x - button_width // 2,
            WINDOW_HEIGHT // 2 + 80,
            button_width,
            button_height,
            "Play Again",
            None
        )
        
        # Main menu button
        self.main_menu_button = Button(
            center_x - button_width // 2,
            WINDOW_HEIGHT // 2 + 160,
            button_width,
            button_height,
            "Main Menu",
            None
        )
    
    def set_game_over(self, winner, game_mode):
        """Set game over state"""
        self.winner = winner
        self.game_mode = game_mode
    
    def handle_event(self, event):
        """Handle game over events"""
        self.play_again_button.handle_event(event)
        self.main_menu_button.handle_event(event)
    
    def update(self):
        """Update game over state"""
        self.play_again_button.update()
        self.main_menu_button.update()
    
    def draw(self, surface):
        """Draw game over overlay"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        surface.blit(overlay, (0, 0))
        
        # Draw game over message
        if self.winner == 'Draw':
            message = "It's a Draw!"
            color = COLOR_TEXT
        elif self.game_mode == 'ai':
            if self.winner == 'X':
                message = "You Win! 🎉"
            else:
                message = "No Mercy. You Lose. 😈"
            color = COLOR_ACCENT if self.winner == 'X' else COLOR_TEXT
        else:
            if self.winner == 'X':
                message = "Player 1 Wins! 🎉"
            else:
                message = "Player 2 Wins! 🎉"
            color = COLOR_ACCENT
        
        # Draw message with wooden panel background
        msg_surface = FONT_MESSAGE.render(message, True, color)
        msg_rect = msg_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Draw panel behind text
        panel_rect = msg_rect.inflate(40, 20)
        pygame.draw.rect(surface, COLOR_BOARD, panel_rect, border_radius=12)
        pygame.draw.rect(surface, COLOR_ACCENT, panel_rect, 3, border_radius=12)
        
        surface.blit(msg_surface, msg_rect)
        
        # Draw buttons
        self.play_again_button.draw(surface)
        self.main_menu_button.draw(surface)
    
    def get_clicked_action(self, pos):
        """Check which button was clicked"""
        if self.play_again_button.rect.collidepoint(pos):
            return "play_again"
        elif self.main_menu_button.rect.collidepoint(pos):
            return "main_menu"
        return None
