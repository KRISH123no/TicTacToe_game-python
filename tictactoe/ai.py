# ai.py - AI opponent logic using Minimax with Alpha-Beta pruning

import random
import copy


class AI:
    """AI opponent using Minimax algorithm with Alpha-Beta pruning"""
    
    def __init__(self, player='O'):
        self.ai_player = player
        self.human_player = 'X' if player == 'O' else 'O'
    
    def get_best_move(self, board):
        """
        Get the best move for AI using Minimax with Alpha-Beta pruning.
        AI plays perfectly - it can only win or draw.
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        empty_cells = board.get_empty_cells()
        
        # Shuffle to add some variety when multiple moves have same score
        random.shuffle(empty_cells)
        
        for row, col in empty_cells:
            # Make temporary move
            board.cells[row][col] = self.ai_player
            
            # Get score using minimax
            score = self.minimax(board, 0, alpha, beta, False)
            
            # Undo move
            board.cells[row][col] = None
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
            
            alpha = max(alpha, best_score)
        
        return best_move
    
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with Alpha-Beta pruning.
        Returns the score for the current board state.
        
        Score values:
        - AI wins: 100
        - Human wins: -100
        - Draw: 0
        """
        # Check for terminal states
        winner = self._check_winner(board)
        
        if winner == self.ai_player:
            return 100 - depth  # Prefer faster wins
        elif winner == self.human_player:
            return -100 + depth  # Delay human wins
        elif board.is_board_full():
            return 0  # Draw
        
        empty_cells = board.get_empty_cells()
        
        if is_maximizing:
            # AI's turn - maximize score
            max_score = float('-inf')
            
            for row, col in empty_cells:
                board.cells[row][col] = self.ai_player
                score = self.minimax(board, depth + 1, alpha, beta, False)
                board.cells[row][col] = None
                
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_score
        else:
            # Human's turn - minimize score (human plays optimally too)
            min_score = float('inf')
            
            for row, col in empty_cells:
                board.cells[row][col] = self.human_player
                score = self.minimax(board, depth + 1, alpha, beta, True)
                board.cells[row][col] = None
                
                min_score = min(score, min_score)
                beta = min(beta, score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_score
    
    def _check_winner(self, board):
        """Check winner on the board"""
        b = board.cells
        
        # Check rows
        for row in range(3):
            if b[row][0] and b[row][0] == b[row][1] == b[row][2]:
                return b[row][0]
        
        # Check columns
        for col in range(3):
            if b[0][col] and b[0][col] == b[1][col] == b[2][col]:
                return b[0][col]
        
        # Check diagonals
        if b[0][0] and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]
        
        # Check for draw
        if board.is_board_full():
            return 'Draw'
        
        return None
