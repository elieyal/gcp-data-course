import os
import google.generativeai as genai
from flask import jsonify, Request
import functions_framework

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def board_to_text(board):
    return "\n".join(f"{r}{c}:{cell or '-'}" for r, row in enumerate(board) for c, cell in enumerate(row))

@functions_framework.http
def get_advice(request: Request):
    try:
        data = request.get_json()
        print("✅ Received data:", data)

        board = data.get("board")
        symbol = data.get("symbol")

        if not board or not symbol or symbol not in ["X", "O"]:
            print("⚠️ Invalid input:", board, symbol)
            return jsonify({"error": "Invalid input"}), 400

        prompt = f"""
You're playing Tic Tac Toe. You're '{symbol}'. The current board is:

{board_to_text(board)}

Suggest the best move in the format "row,col – explanation".
"""

        print("📤 Prompt to Gemini:", prompt)

        response = model.generate_content(prompt)

        print("✅ Gemini response:", response.text.strip())

        return jsonify({"advice": response.text.strip()})

    except Exception as e:
        print("💥 Gemini error:", str(e))
        return jsonify({"error": str(e)}), 500