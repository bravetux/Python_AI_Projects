# 🎮 Tic Tac Toe — Powered by Gemini AI

A smart, strategic, and *borderline unbeatable* Tic Tac Toe game built with Python and Gemini API integration.  
The AI doesn’t just play — it *analyzes*, *predicts*, and *counteracts* your moves using pattern recognition and minimax-like logic powered by **Google Gemini**.  

---

## 🚀 Features

- 💡 **Gemini AI Integration** — Uses `gemini-1.5-flash` (or upgradeable model) for dynamic board evaluation.  
- 🧠 **High-Level Strategy** — AI scans for winning combinations, potential forks, and defensive moves.  
- 🕹️ **Interactive CLI Interface** — Play directly in the terminal with clean prompts and board updates.  
- ⚙️ **Customizable Difficulty (optional)** — Adjust prompt complexity or API logic for different challenge levels.  
- 🔄 **Replay Option** — Restart without reloading the script.  

---

## 🧩 Gameplay

You play as `X`, and Gemini plays as `O`.  
Take turns entering your move (1–9), corresponding to the grid:

1 | 2 | 3
4 | 5 | 6
7 | 8 | 9


**Objective:** Get three of your symbols in a row — horizontally, vertically, or diagonally.

---

## 🧠 How Gemini Thinks

Instead of hardcoding every possible outcome, Gemini evaluates the **current board** and **predicts optimal moves** using pattern-based reasoning.  
It looks for:
- Immediate wins 🏆  
- Blocking player wins 🚫  
- Fork opportunities 🔁  
- Strategic center and corner control 🎯  

This makes the AI harder to beat and more human-like in play.

---

## 🧰 Setup Instructions

### 1️⃣ Prerequisites

- Python 3.9+  
- `google-generativeai` library  
- A valid `GEMINI_API_KEY`

### 2️⃣ Installation

```bash
pip install google-generativeai

### 3️⃣ Set Your API Key
On Linux/macOS:
export GEMINI_API_KEY="your_api_key_here"

On Windows:
setx GEMINI_API_KEY "your_api_key_here"

### 4️⃣ Run the Game
python tic_tac_toe_gemini.py

===== 🤖 GEMINI TIC TAC TOE =====
Choose difficulty: easy | medium | hard
Enter difficulty: hard

Fetching AI strategy from Gemini...

You are X | Gemini is O

 0,0 | 0,1 | 0,2
-----------------
 1,0 | 1,1 | 1,2
-----------------
 2,0 | 2,1 | 2,2

Enter your move (row,col):

You: X
Gemini: O

 X |   |  
-----------
   | O |  
-----------
   |   |  

Gemini: “I’ll take the center — classic control strategy.”


