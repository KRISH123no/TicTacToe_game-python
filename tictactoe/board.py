# board.py - Board rendering and logic

import pygame
from settings import *


class Board:
    """Manages the tic-tac-toe board state and rendering"""
    
    def __init__(self):
        self.cells = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.animation_progress = {}  # Track animation for each cell
        self.winning_line = None  # Tuple of ((start_row, start_col), (end_row, end_col))
        self.win_line_progress = 0
        self.winner = None
        self.winning_cells = []
        
    def reset(self):
        """Reset the board for a new game"""
        self.cells = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.animation_progress = {}
        self.winning_line = None
        self.win_line_progress = 0
        self.winner = None
        self.winning_cells = []
    
    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.cells[row][col] is None
    
    def make_move(self, row, col, player):
        """Place a mark on the board"""
        if self.is_valid_move(row, col):
            self.cells[row][col] = player
            self.animation_progress[(row, col)] = 0
            return True
        return False
    
    def check_winner(self):
        """Check if there's a winner or draw"""
        board = self.cells
        
        # Check rows
        for row in range(BOARD_SIZE):
            if board[row][0] and board[row][0] == board[row][1] == board[row][2]:
                self.winner = board[row][0]
                self.winning_cells = [(row, 0), (row, 1), (row, 2)]
                self.winning_line = ((row, 0), (row, 2))
                return self.winner
        
        # Check columns
        for col in range(BOARD_SIZE):
            if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
                self.winner = board[0][col]
                self.winning_cells = [(0, col), (1, col), (2, col)]
                self.winning_line = ((0, col), (2, col))
                return self.winner
        
        # Check diagonals
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            self.winner = board[0][0]
            self.winning_cells = [(0, 0), (1, 1), (2, 2)]
            self.winning_line = ((0, 0), (2, 2))
            return self.winner
        
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            self.winner = board[0][2]
            self.winning_cells = [(0, 2), (1, 1), (2, 0)]
            self.winning_line = ((0, 2), (2, 0))
            return self.winner
        
        # Check for draw
        if self.is_board_full():
            return 'Draw'
        
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.cells[row][col] is None:
                    return False
        return True
    
    def get_empty_cells(self):
        """Return list of empty cell positions"""
        empty = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.cells[row][col] is None:
                    empty.append((row, col))
        return empty
    
    def get_cell_rect(self, row, col):
        """Get the rectangle for a cell"""
        x = BOARD_OFFSET_X + col * (CELL_SIZE + 10)
        y = BOARD_OFFSET_Y + row * (CELL_SIZE + 10)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    
    def get_cell_from_pos(self, pos):
        """Convert screen position to cell coordinates"""
        x, y = pos
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_rect = self.get_cell_rect(row, col)
                if cell_rect.collidepoint(x, y):
                    return row, col
        return None
    
    def update_animations(self, dt):
        """Update animation progress"""
        # Update mark animations
        for key in list(self.animation_progress.keys()):
            self.animation_progress[key] += dt / ANIMATION_DURATION
            if self.animation_progress[key] >= 1:
                del self.animation_progress[key]
        
        # Update winning line animation
        if self.winning_line and self.win_line_progress < 1:
            self.win_line_progress += dt / WIN_LINE_DURATION
            if self.win_line_progress > 1:
                self.win_line_progress = 1
    
    def draw(self, surface, hovered_cell=None):
        """Draw the game board"""
        # Draw board background (wooden panel)
        board_width = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE - 1) * 10 + 40
        board_height = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE - 1) * 10 + 40
        board_rect = pygame.Rect(
            BOARD_OFFSET_X - 20,
            BOARD_OFFSET_Y - 20,
            board_width,
            board_height
        )
        
        # Draw wooden board background with gradient
        pygame.draw.rect(surface, COLOR_BOARD, board_rect, border_radius=12)
        
        # Draw inner shadow/border effect
        pygame.draw.rect(surface, (30, 15, 8), board_rect.inflate(-8, -8), border_radius=8)
        
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Vertical lines
            x = BOARD_OFFSET_X + i * CELL_SIZE + (i - 1) * 10
            pygame.draw.line(surface, COLOR_GRID, (x, BOARD_OFFSET_Y), 
                           (x, BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE + (BOARD_SIZE - 1) * 10), 6)
            # Horizontal lines
            y = BOARD_OFFSET_Y + i * CELL_SIZE + (i - 1) * 10
            pygame.draw.line(surface, COLOR_GRID, (BOARD_OFFSET_X, y),
                           (BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + (BOARD_SIZE - 1) * 10, y), 6)
        
        # Draw cell highlights (hover effect)
        if hovered_cell:
            row, col = hovered_cell
            if self.cells[row][col] is None:
                cell_rect = self.get_cell_rect(row, col)
                # Draw subtle amber glow
                glow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*COLOR_ACCENT, 40), glow_surface.get_rect())
                surface.blit(glow_surface, cell_rect.topleft)
        
        # Draw marks
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                player = self.cells[row][col]
                if player:
                    cell_rect = self.get_cell_rect(row, col)
                    center = cell_rect.center
                    
                    # Get animation progress
                    progress = self.animation_progress.get((row, col), 1)
                    
                    if player == 'X':
                        self._draw_x(surface, center, progress)
                    else:
                        self._draw_o(surface, center, progress)
        
        # Draw winning line
        if self.winning_line and self.win_line_progress > 0:
            self._draw_winning_line(surface)
    
    def _draw_x(self, surface, center, progress):
        """Draw X mark with animation"""
        size = 45
        offset = size * progress
            
        # Draw two crossing lines with bold stroke
        # Line 1: top-left to bottom-right
        start1 = (center[0] - offset, center[1] - offset)
        end1 = (center[0] + offset, center[1] + offset)
        pygame.draw.line(surface, COLOR_X_MARK, start1, end1, 8)
        
        # Line 2: top-right to bottom-left
        start2 = (center[0] + offset, center[1] - offset)
        end2 = (center[0] - offset, center[1] + offset)
        pygame.draw.line(surface, COLOR_X_MARK, start2, end2, 8)
    
    def _draw_o(self, surface, center, progress):
        """Draw O mark with animation"""
        radius = int(45 * progress)
        if radius > 0:
            # Draw circle with bold stroke
            pygame.draw.circle(surface, COLOR_O_MARK, center, radius, 8)
    
    def _draw_winning_line(self, surface):
        """Draw winning line across winning cells"""
        if not self.winning_line:
            return
            
        start_cell, end_cell = self.winning_line
        start_rect = self.get_cell_rect(start_cell[0], start_cell[1])
        end_rect = self.get_cell_rect(end_cell[0], end_cell[1])
        
        start_pos = start_rect.center
        end_pos = end_rect.center
        
        # Calculate animated end position
        current_end = (
            start_pos[0] + (end_pos[0] - start_pos[0]) * self.win_line_progress,
            start_pos[1] + (end_pos[1] - start_pos[1]) * self.win_line_progress
        )
        
        # Draw winning line with glow effect
        # Outer glow
        pygame.draw.line(surface, (*COLOR_ACCENT, 100), start_pos, current_end, 16)
        # Main line
        pygame.draw.line(surface, COLOR_ACCENT, start_pos, current_end, 8)
        
        # Draw winning cell overlays
        for row, col in self.winning_cells:
            cell_rect = self.get_cell_rect(row, col)
            overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*COLOR_ACCENT, 50), overlay.get_rect())
            surface.blit(overlay, cell_rect.topleft)
