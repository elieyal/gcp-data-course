#! /usr/bin/python3

import os
import google.generativeai as genai

API_KEY = "<Gemin API key here>" #os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Please set GEMINI_API_KEY as an environment variable.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-pro" if you have access

# Game functions
def print_board(board):
    print("\nBoard:")
    for row in board:
        print(" | ".join(cell or " " for cell in row))
        print("-" * 9)

def board_to_text(board):
    return "\n".join(f"{r}{c}:{cell or '-'}" for r, row in enumerate(board) for c, cell in enumerate(row))

def check_winner(board, symbol):
    lines = [
        [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
    ]
    return any(all(board[r][c] == symbol for r, c in line) for line in lines)

def get_gemini_advice(board, symbol):
    prompt = f"""
You're playing Tic Tac Toe. You're '{symbol}'. The current board is:

{board_to_text(board)}

Suggest the best move in the format "row,col – explanation".
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error getting advice: {str(e)}"

def is_valid_move(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None

def main():
    board = [[None for _ in range(3)] for _ in range(3)]
    current = "X"

    while True:
        print_board(board)

        # Check for game end
        if check_winner(board, "X"):
            print("Player X wins!")
            break
        if check_winner(board, "O"):
            print("Player O wins!")
            break
        if all(cell for row in board for cell in row):
            print("It's a tie!")
            break

        move = input(f"Player {current}, enter your move (e.g., 01), or type 'ADVICE!': ").strip()

        if move.upper() == "ADVICE!":
            advice = get_gemini_advice(board, current)
            print(f"\n💡 Gemini's advice for Player {current}: {advice}\n")
            move = input(f"Now enter your move (e.g., 01): ").strip()

        if len(move) == 2 and move.isdigit():
            row, col = int(move[0]), int(move[1])
            if is_valid_move(board, row, col):
                board[row][col] = current
                current = "O" if current == "X" else "X"
            else:
                print("Invalid move: Cell is occupied or out of range.")
        else:
            print("Invalid input. Enter row and column as two digits (e.g., 01).")

if __name__ == "__main__":
    main()