# game.py - Core gameplay logic

import pygame
from settings import *
from board import Board
from ai import AI


class Game:
    """Manages the core game logic"""
    
    def __init__(self, game_mode, first_player='X'):
        self.game_mode = game_mode  # 'ai' or 'multiplayer'
        self.first_player = first_player
        self.current_player = first_player
        self.board = Board()
        self.ai = AI(player='O') if game_mode == 'ai' else None
        self.winner = None
        self.is_game_over = False
        self.hovered_cell = None
        self.ai_thinking = False
        self.ai_think_start_time = 0
        self.ai_message_timer = 0
        self.ai_message = ""
        self.message_timer = 0
        self.message = ""
        self.selected_cell = None  # For keyboard navigation
        self.game_start_time = 0
        
    def reset(self, first_player=None):
        """Reset game for a new round"""
        if first_player:
            self.first_player = first_player
        self.current_player = self.first_player
        self.board.reset()
        self.winner = None
        self.is_game_over = False
        self.ai_thinking = False
        self.ai_message = ""
        self.message = ""
        self.selected_cell = None
        
    def handle_event(self, event):
        """Handle game events"""
        if self.is_game_over:
            return None
        
        if event.type == pygame.MOUSEMOTION:
            # Update hovered cell
            cell = self.board.get_cell_from_pos(event.pos)
            if cell and self.board.is_valid_move(cell[0], cell[1]):
                self.hovered_cell = cell
            else:
                self.hovered_cell = None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                cell = self.board.get_cell_from_pos(event.pos)
                if cell:
                    return self._make_move(cell[0], cell[1])
        
        if event.type == pygame.KEYDOWN:
            return self._handle_keyboard(event.key)
        
        return None
    
    def _handle_keyboard(self, key):
        """Handle keyboard input for navigation and placement"""
        if self.selected_cell is None:
            self.selected_cell = (1, 1)  # Start at center
        else:
            row, col = self.selected_cell
            
            if key == pygame.K_UP and row > 0:
                row -= 1
            elif key == pygame.K_DOWN and row < 2:
                row += 1
            elif key == pygame.K_LEFT and col > 0:
                col -= 1
            elif key == pygame.K_RIGHT and col < 2:
                col += 1
            elif key == pygame.K_RETURN:
                # Try to place mark at selected cell
                if self.board.is_valid_move(row, col):
                    return self._make_move(row, col)
            
            self.selected_cell = (row, col)
        
        return None
    
    def _make_move(self, row, col):
        """Make a move on the board"""
        if self.board.is_valid_move(row, col) and not self.ai_thinking:
            self.board.make_move(row, col, self.current_player)
            self.selected_cell = None
            
            # Check for win/draw
            result = self.board.check_winner()
            
            if result:
                self._handle_game_end(result)
            else:
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                # If playing against AI and it's AI's turn
                if self.game_mode == 'ai' and self.current_player == 'O':
                    self.ai_thinking = True
                    self.ai_think_start_time = pygame.time.get_ticks()
            
            return True
        
        return False
    
    def _handle_game_end(self, result):
        """Handle game end state"""
        if result == 'Draw':
            self.winner = 'Draw'
            self.is_game_over = True
        else:
            self.winner = result
            self.is_game_over = True
    
    def update(self, current_time):
        """Update game state"""
        # Update board animations
        dt = 16  # Approximate frame time at 60 FPS
        self.board.update_animations(dt)
        
        # Handle AI thinking
        if self.ai_thinking and not self.is_game_over:
            elapsed = current_time - self.ai_think_start_time
            
            if elapsed >= AI_THINK_DELAY:
                self.ai_thinking = False
                self._ai_make_move()
        
        # Update messages
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
    
    def _ai_make_move(self):
        """AI makes its move"""
        if self.is_game_over:
            return
            
        # Get best move
        move = self.ai.get_best_move(self.board)
        
        if move:
            row, col = move
            self.board.make_move(row, col, 'O')
            
            # Check for win/draw
            result = self.board.check_winner()
            
            if result:
                self._handle_game_end(result)
                if self.winner == 'O':
                    self.ai_message = "No mercy. 😈"
                    self.ai_message_timer = 2000
            else:
                self.current_player = 'X'
    
    def get_turn_text(self):
        """Get text for current turn"""
        if self.game_mode == 'ai':
            if self.current_player == 'X':
                return "Player X's Turn"
            else:
                return "Bot's Turn"
        else:
            if self.current_player == 'X':
                return "Player 1's Turn"
            else:
                return "Player 2's Turn"
    
    def get_game_over_text(self):
        """Get game over message"""
        if self.winner == 'Draw':
            return "It's a Draw!"
        
        if self.game_mode == 'ai':
            if self.winner == 'X':
                return "You Win! 🎉"
            else:
                return "No Mercy. You Lose. 😈"
        else:
            if self.winner == 'X':
                return "Player 1 Wins! 🎉"
            else:
                return "Player 2 Wins! 🎉"
    
    def draw(self, surface):
        """Draw the game"""
        # Draw board
        self.board.draw(surface, self.hovered_cell)
        
        # Draw selected cell highlight (keyboard navigation)
        if self.selected_cell:
            cell_rect = self.board.get_cell_rect(self.selected_cell[0], self.selected_cell[1])
            pygame.draw.rect(surface, COLOR_ACCENT, cell_rect, 3)
        
        # Draw turn indicator
        if not self.is_game_over:
            turn_text = self.get_turn_text()
            text_surface = FONT_SUBTITLE.render(turn_text, True, COLOR_TEXT)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 100))
            surface.blit(text_surface, text_rect)
            
            # Draw AI thinking message
            if self.ai_thinking:
                ai_text = "AI is thinking..."
                ai_surface = FONT_SCORE.render(ai_text, True, COLOR_TEXT)
                ai_rect = ai_surface.get_rect(center=(WINDOW_WIDTH // 2, 130))
                surface.blit(ai_surface, ai_rect)
        
        # Draw AI victory message
        if self.ai_message:
            ai_msg_surface = FONT_MESSAGE.render(self.ai_message, True, COLOR_ACCENT)
            ai_msg_rect = ai_msg_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            surface.blit(ai_msg_surface, ai_msg_rect)
        
        # Draw bottom hint
        hint_surface = FONT_HINT.render("Press R to restart", True, COLOR_TEXT)
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        surface.blit(hint_surface, hint_rect)
