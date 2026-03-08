# settings.py - Global constants and configuration

import pygame

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
FPS = 60
WINDOW_TITLE = "Tic Tac Toe"

# Color palette - Wooden Tavern Theme
COLOR_BACKGROUND = (107, 58, 42)       # #6B3A2A - warm medium brown
COLOR_BOARD = (61, 31, 16)             # #3D1F10 - dark brown
COLOR_GRID = (139, 94, 60)             # #8B5E3C - medium wood brown
COLOR_ACCENT = (200, 134, 10)          # #C8860A - amber gold
COLOR_X_MARK = (0, 0, 0)               # #000000 - pure black
COLOR_O_MARK = (255, 255, 255)         # #FFFFFF - pure white
COLOR_TEXT = (245, 222, 179)           # #F5DEB3 - cream
COLOR_BUTTON_HOVER = (80, 45, 25)      # Lighter brown for hover
COLOR_BUTTON = (61, 31, 16)            # Dark brown for buttons
COLOR_OVERLAY = (0, 0, 0, 180)         # Semi-transparent black

# Board settings
BOARD_SIZE = 3
CELL_SIZE = 150
BOARD_PADDING = 20
BOARD_OFFSET_X = (WINDOW_WIDTH - (BOARD_SIZE * CELL_SIZE + (BOARD_SIZE - 1) * 10)) // 2
BOARD_OFFSET_Y = 150

# Animation settings
ANIMATION_DURATION = 200  # milliseconds for mark drawing
WIN_LINE_DURATION = 500   # milliseconds for winning line
AI_THINK_DELAY = 800      # milliseconds

# Font settings
pygame.font.init()
FONT_TITLE = pygame.font.Font(None, 72)
FONT_SUBTITLE = pygame.font.Font(None, 48)
FONT_BUTTON = pygame.font.Font(None, 42)
FONT_SCORE = pygame.font.Font(None, 36)
FONT_HINT = pygame.font.Font(None, 24)
FONT_MESSAGE = pygame.font.Font(None, 56)

# Game states
STATE_MAIN_MENU = "main_menu"
STATE_SETTINGS = "settings"
STATE_GAME = "game"
STATE_GAME_OVER = "game_over"
