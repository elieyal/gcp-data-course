#! /usr/bin/python3

from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)


API_KEY = "<Gemin API key here>" #os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise EnvironmentError("Set GEMINI_API_KEY env var")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash") 

def board_to_text(board):
    return "\n".join(f"{r}{c}:{cell or '-'}" for r, row in enumerate(board) for c, cell in enumerate(row))

@app.route("/advice", methods=["POST"])
def get_advice():
    data = request.json
    board = data.get("board")
    symbol = data.get("symbol")

    if not board or not symbol or symbol not in ["X", "O"]:
        return jsonify({"error": "Invalid request. Requires 'board' (3x3 list) and 'symbol' ('X' or 'O')"}), 400

    prompt = f"""
You're playing Tic Tac Toe. You're '{symbol}'. The current board is:

{board_to_text(board)}

Suggest the best move in the format "row,col – explanation".
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"advice": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)