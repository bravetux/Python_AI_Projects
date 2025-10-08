#!/usr/bin/env python3
"""
Gemini Tic Tac Toe — AI with strategic fallback (Minimax + Gemini Hybrid)

Features:
- Gemini-powered AI decision-making
- Minimax algorithm fallback (perfect play)
- Human vs AI with adjustable difficulty
"""

import os
import re
import time
import random
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_KEY_HERE")

# --- Board utilities ---
def print_board(board):
    print("\n")
    for r in range(3):
        print(" | ".join(board[r]))
        if r < 2:
            print("---------")
    print("\n")

def check_win(board, symbol):
    # Rows / Cols / Diagonals
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)): return True
        if all(board[j][i] == symbol for j in range(3)): return True
    if all(board[i][i] == symbol for i in range(3)): return True
    if all(board[i][2 - i] == symbol for i in range(3)): return True
    return False

def is_full(board):
    return all(board[r][c] != " " for r in range(3) for c in range(3))

def available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

# --- Minimax (perfect fallback AI) ---
def minimax(board, depth, is_max, ai_symbol, human_symbol):
    if check_win(board, ai_symbol): return 10 - depth
    if check_win(board, human_symbol): return depth - 10
    if is_full(board): return 0

    if is_max:
        best = -999
        for (r, c) in available_moves(board):
            board[r][c] = ai_symbol
            score = minimax(board, depth + 1, False, ai_symbol, human_symbol)
            board[r][c] = " "
            best = max(best, score)
        return best
    else:
        best = 999
        for (r, c) in available_moves(board):
            board[r][c] = human_symbol
            score = minimax(board, depth + 1, True, ai_symbol, human_symbol)
            board[r][c] = " "
            best = min(best, score)
        return best

def best_move_minimax(board, ai_symbol, human_symbol):
    best_val = -999
    best_move = None
    for (r, c) in available_moves(board):
        board[r][c] = ai_symbol
        move_val = minimax(board, 0, False, ai_symbol, human_symbol)
        board[r][c] = " "
        if move_val > best_val:
            best_val = move_val
            best_move = (r, c)
    return best_move

# --- Gemini Move Fetch ---
def get_board_text(board):
    return "\n".join("".join(cell if cell != " " else "." for cell in row) for row in board)

def parse_move_from_text(text):
    match = re.search(r"([0-2])\s*[,\s]\s*([0-2])", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

def get_gemini_move(board, difficulty, ai_symbol, human_symbol):
    board_text = get_board_text(board)
    prompt = f"""
You are a highly skilled Tic Tac Toe AI.
Current board ('.' = empty):
{board_text}

You are '{ai_symbol}'. Opponent is '{human_symbol}'.
Think strategically:
- Prioritize winning moves.
- Block the opponent's winning move.
- Control center and corners for advantage.
- For hard mode, assume perfect opponent play.

Return exactly one move as "row,col" (0-based). No text, no JSON, just the move.
Difficulty: {difficulty}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        text = response.text.strip()
        move = parse_move_from_text(text)

        if move and move in available_moves(board):
            return move
        print("⚠️ Gemini move invalid, falling back to minimax.")
    except Exception as e:
        print(f"⚠️ Gemini request failed: {e}")

    return best_move_minimax(board, ai_symbol, human_symbol)

# --- Human Input ---
def human_move(board):
    while True:
        raw = input("Enter your move (row,col): ").strip()
        match = re.search(r"([0-2])\s*[,\s]\s*([0-2])", raw)
        if not match:
            print("❌ Invalid input. Try '1,2'.")
            continue
        r, c = int(match.group(1)), int(match.group(2))
        if board[r][c] != " ":
            print("❌ That cell is taken.")
            continue
        return r, c

# --- Game Loop ---
def play_game(difficulty="hard", starting="human"):
    board = [[" " for _ in range(3)] for _ in range(3)]
    human_symbol = input("Choose your symbol (X or O): ").strip().upper()
    if human_symbol not in ["X", "O"]:
        human_symbol = "X"
    ai_symbol = "O" if human_symbol == "X" else "X"

    print(f"\nYou are {human_symbol}, Gemini is {ai_symbol}. Difficulty: {difficulty}")
    print_board(board)

    turn = starting
    while True:
        if turn == "human":
            r, c = human_move(board)
            board[r][c] = human_symbol
        else:
            print("🤖 Gemini is thinking...", end="", flush=True)
            for _ in range(2):
                time.sleep(0.4)
                print(".", end="", flush=True)
            print()
            move = get_gemini_move(board, difficulty, ai_symbol, human_symbol)
            if move is None:
                move = best_move_minimax(board, ai_symbol, human_symbol)
            r, c = move
            board[r][c] = ai_symbol

        print_board(board)

        # Check game state
        if check_win(board, human_symbol):
            print("🎉 You win! Well played.")
            break
        elif check_win(board, ai_symbol):
            print("☠️ Gemini wins. Perfect play.")
            break
        elif is_full(board):
            print("🤝 It's a draw.")
            break

        turn = "ai" if turn == "human" else "human"

# --- Entry Point ---
def main():
    print("===== ♟️ GEMINI TIC TAC TOE PRO =====")
    difficulty = input("Difficulty (easy | medium | hard) [hard]: ").strip().lower() or "hard"
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "hard"

    starter = input("Who starts first? (me | gemini) [me]: ").strip().lower() or "me"
    play_game(difficulty, "human" if starter in ["me", "human"] else "ai")

if __name__ == "__main__":
    main()
