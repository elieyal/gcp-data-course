#! /usr/bin/python3

import requests

ADVICE_URL = "<Cloud Run function URL Here!!>"

def print_board(board):
    print("\nBoard:")
    for row in board:
        print(" | ".join(cell or " " for cell in row))
        print("-" * 9)

def check_winner(board, symbol):
    lines = [
        [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
    ]
    return any(all(board[r][c] == symbol for r, c in line) for line in lines)

def is_valid_move(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None

def get_advice_from_server(board, symbol):
    try:
        res = requests.post(ADVICE_URL, json={"board": board, "symbol": symbol})
        res.raise_for_status()
        return res.json().get("advice", "No advice received.")
    except Exception as e:
        return f"Error contacting advice service: {e}"

def main():
    board = [[None for _ in range(3)] for _ in range(3)]
    current = "X"

    while True:
        print_board(board)

        if check_winner(board, "X"):
            print("Player X wins!")
            break
        if check_winner(board, "O"):
            print("Player O wins!")
            break
        if all(cell for row in board for cell in row):
            print("It's a tie!")
            break

        move = input(f"Player {current}, enter move (e.g., 01), or 'ADVICE!': ").strip()

        if move.upper() == "ADVICE!":
            advice = get_advice_from_server(board, current)
            print(f"💡 Advice for {current}: {advice}")
            move = input("Now enter your move (e.g., 01): ").strip()

        if len(move) == 2 and move.isdigit():
            row, col = int(move[0]), int(move[1])
            if is_valid_move(board, row, col):
                board[row][col] = current
                current = "O" if current == "X" else "X"
            else:
                print("Invalid or occupied cell!")
        else:
            print("Invalid input. Use rowcol format like 01 or type ADVICE!")

if __name__ == "__main__":
    main()