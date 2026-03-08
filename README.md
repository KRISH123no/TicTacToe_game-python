# ⭕ Tic Tac Toe - Wooden Tavern Edition

A desktop Tic Tac Toe game built with Python and pygame featuring an unbeatable Minimax AI and local multiplayer, wrapped in a warm wooden tavern aesthetic.

---

## 🎮 Features

- **vs AI** — Play against a ruthless unbeatable AI (Minimax + Alpha-Beta pruning)
- **vs Friend** — Local 2-player multiplayer on the same computer
- **Unbeatable AI** — Full Minimax algorithm, can only win or draw, never loses
- **Score Tracker** — Persists across rematches in the same session
- **Smooth Animations** — X and O draw with smooth line animations
- **Winning Line** — Highlighted in amber gold when game ends
- **Wooden Tavern UI** — Rich dark brown theme with amber gold accents
- **Hover Effects** — Cells glow on hover for better UX
- **Keyboard Support** — Arrow keys to navigate, Enter to place

---

## 🛠️ Requirements

```
Python 3.9+
pygame
```

Install dependencies:
```bash
pip3 install pygame
```

---

## 🚀 How to Run

```bash
cd tictactoe
python3 main.py
```

---

## 📁 Project Structure

```
tictactoe/
├── main.py        # Entry point and main game loop
├── game.py        # Core gameplay logic
├── board.py       # Board rendering and win detection
├── ai.py          # Minimax AI with Alpha-Beta pruning
├── menu.py        # Main menu and navigation
├── settings.py    # Global constants and configuration
└── ui.py          # UI elements and score display
```

---

## 🎯 Controls

**Mouse:**
- Click a cell to place your mark

**Keyboard:**
- Arrow keys to navigate cells
- Enter to confirm placement
- R to restart
- ESC to go back to menu

---

## 🤖 About the AI

The AI uses the **Minimax algorithm with Alpha-Beta pruning** — it explores every possible future game state and always picks the optimal move. On a 3x3 board this means the AI is mathematically perfect and **cannot be beaten**, only drawn against if you play perfectly.

---

Built with ❤️ using Python and pygame
