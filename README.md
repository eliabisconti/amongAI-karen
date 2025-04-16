# AmongAI-Karen

**AmongAI-Karen** is a PC game developed as part of the *Smart Applications* course at the Department of Computer Science, University of Pisa, under the supervision of Prof. Vincenzo Gervasi.

Inspired by the well-known game *Among Us*, the project was designed to allow the development and testing of AI agents in a multiplayer, social-deception environment — later extended to support human players as well.

---

## Game Overview

- **Multiplayer match-based structure**: Two teams compete to **capture the opponent’s flag** and **eliminate enemies**.
- Players can be **"impostors"** trying to sabotage the team — leading to a **social game mechanic** where agents (or humans) must detect and vote to eliminate the impostor.
- Includes a **"Turing Game"** mode where the objective is to correctly classify each player as AI or human.
- Fully playable via **chat interface** and UI.

---

## AI & Karen: NLP Module

A standout feature of the project is the **Karen module** — an AI designed to respond to misogynistic language detected in chat.

- Uses NLP to **analyze in-game messages** in real time.
- Detects misogynistic or offensive phrases based on an custom offensive language detection model
- When detected, the **Karen AI** responds with pre-programmed phrases, taking a stand against toxic behavior.
- Demonstrates integration of **socially aware AI** into gaming environments.

---

## 🛠 Tech Stack

- Python (core scripting and AI logic)
- Pygame / custom game engine (for visuals and interaction)
- Scikit-learn, Regex / NLP tools (for chat analysis)
- Agile development workflow, developed collaboratively in team of three
