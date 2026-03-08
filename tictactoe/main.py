# main.py - Entry point and main game loop

import pygame
import sys
from settings import *
from menu import Menu, SettingsMenu, GameOverScreen
from game import Game
from ui import ScoreTracker, drawWoodenBackground


class GameApp:
    """Main application class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = STATE_MAIN_MENU
        self.game_mode = None
        self.first_player = 'X'
        
        # Create components
        self.menu = Menu()
        self.settings_menu = SettingsMenu(self.first_player)
        self.game_over_screen = GameOverScreen()
        self.game = None
        self.score_tracker = ScoreTracker()
        
        # Fonts need to be re-initialized after pygame init
        global FONT_TITLE, FONT_SUBTITLE, FONT_BUTTON, FONT_SCORE, FONT_HINT, FONT_MESSAGE
        FONT_TITLE = pygame.font.Font(None, 72)
        FONT_SUBTITLE = pygame.font.Font(None, 48)
        FONT_BUTTON = pygame.font.Font(None, 42)
        FONT_SCORE = pygame.font.Font(None, 36)
        FONT_HINT = pygame.font.Font(None, 24)
        FONT_MESSAGE = pygame.font.Font(None, 56)
        
        # Re-create menus with new fonts
        self.menu = Menu()
        self.settings_menu = SettingsMenu(self.first_player)
        self.game_over_screen = GameOverScreen()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self._handle_event(event)
            
            # Update
            self._update(current_time)
            
            # Draw
            self._draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_event(self, event):
        """Handle events based on current state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == STATE_SETTINGS:
                    self.state = STATE_MAIN_MENU
                elif self.state == STATE_GAME:
                    self.state = STATE_MAIN_MENU
                    self.score_tracker.reset()
            
            # R to restart during game
            if event.key == pygame.K_r and self.state == STATE_GAME:
                if self.game:
                    self.game.reset(self.first_player)
        
        if self.state == STATE_MAIN_MENU:
            self._handle_main_menu_event(event)
        
        elif self.state == STATE_SETTINGS:
            self._handle_settings_event(event)
        
        elif self.state == STATE_GAME:
            self._handle_game_event(event)
        
        elif self.state == STATE_GAME_OVER:
            self._handle_game_over_event(event)
    
    def _handle_main_menu_event(self, event):
        """Handle main menu events"""
        self.menu.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            # Check for mode selection
            mode = self.menu.get_clicked_button(pos)
            if mode:
                self.game_mode = mode
                self._start_game()
                return
            
            # Check for settings
            if self.menu.is_settings_clicked(pos):
                self.state = STATE_SETTINGS
    
    def _handle_settings_event(self, event):
        """Handle settings menu events"""
        self.settings_menu.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.settings_menu.is_back_clicked(pos):
                self.first_player = self.settings_menu.first_player
                self.state = STATE_MAIN_MENU
    
    def _handle_game_event(self, event):
        """Handle game events"""
        if self.game:
            result = self.game.handle_event(event)
            
            # Handle restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game.reset(self.first_player)
    
    def _handle_game_over_event(self, event):
        """Handle game over events"""
        self.game_over_screen.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            action = self.game_over_screen.get_clicked_action(pos)
            
            if action == "play_again":
                self._start_game()
            elif action == "main_menu":
                self.score_tracker.reset()
                self.state = STATE_MAIN_MENU
    
    def _update(self, current_time):
        """Update game state"""
        if self.state == STATE_MAIN_MENU:
            self.menu.update()
        
        elif self.state == STATE_SETTINGS:
            self.settings_menu.update()
        
        elif self.state == STATE_GAME:
            if self.game:
                self.game.update(current_time)
                
                # Check if game just ended
                if self.game.is_game_over and not self.game.winner:
                    # This shouldn't happen but just in case
                    pass
                elif self.game.is_game_over and self.game.winner:
                    # Update score and show game over
                    if self.game.winner != 'Draw':
                        self.score_tracker.add_win(self.game.winner)
                    else:
                        self.score_tracker.add_win('Draw')
                    self.game_over_screen.set_game_over(self.game.winner, self.game_mode)
                    self.state = STATE_GAME_OVER
        
        elif self.state == STATE_GAME_OVER:
            self.game_over_screen.update()
    
    def _draw(self):
        """Draw the screen based on current state"""
        if self.state == STATE_MAIN_MENU:
            self.menu.draw(self.screen)
        
        elif self.state == STATE_SETTINGS:
            self.settings_menu.draw(self.screen)
        
        elif self.state == STATE_GAME:
            # Draw wooden background
            drawWoodenBackground(self.screen)
            
            # Draw score tracker
            self.score_tracker.draw(self.screen, self.game_mode)
            
            # Draw game
            if self.game:
                self.game.draw(self.screen)
        
        elif self.state == STATE_GAME_OVER:
            # Draw game first
            drawWoodenBackground(self.screen)
            if self.game:
                self.score_tracker.draw(self.screen, self.game_mode)
                self.game.draw(self.screen)
            
            # Draw game over overlay
            self.game_over_screen.draw(self.screen)
        
        pygame.display.flip()
    
    def _start_game(self):
        """Start a new game"""
        self.game = Game(self.game_mode, self.first_player)
        self.state = STATE_GAME


def main():
    """Main entry point"""
    app = GameApp()
    app.run()


if __name__ == "__main__":
    main()
