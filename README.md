# 🔴 Connect 4: Turbo Edition (Python + C++)

A high-performance Connect Four game featuring a polished Python `tkinter` GUI powered by a **compiled C++ backend**.

This project demonstrates a hybrid architecture: the game logic and UI run in Python for flexibility, while the AI computation is offloaded to a custom C++ engine (`pybind11`) for maximum speed.

## 🚀 Features

* **Hybrid Engine:**
    * **Python:** Handles UI, state management, and easier AI levels.
    * **C++:** Handles the "Hard" and "Impossible" AI using a highly optimized Minimax algorithm with Alpha-Beta pruning.
* **4 Difficulty Levels:**
    * **Easy:** Random moves (for kids).
    * **Medium:** Blocks winning moves and takes immediate wins.
    * **Hard:** Uses C++ engine (Depth 5) for tactical play.
    * **Impossible:** Uses C++ engine (Depth 9) for **god-like play**. Calculates ~40 million positions instantly.
* **Zero-Setup Install:** The repository includes a pre-compiled binary wheel. The game automatically installs the C++ engine when you run it—**no compiler required.**
* **Interactive GUI:**
    * **Ghost Piece:** Hover over columns to see exactly where your piece will land.
    * **Live Updates:** Highlights the last move for clarity.
    * **Menu System:** Change difficulty on the fly.

## 📸 Screenshots

<img src="game_ss.png" width="40%" alt="Connect Four Game Board">

## 🛠️ Architecture

This project uses a layered architecture to separate concerns:

* **UI Layer (`ui/`):** Tkinter-based interface.
* **Service Layer (`services/`):** Game coordinator (`game.py`) that syncs the Python board with the C++ engine.
* **Core Engine (`services/connect4_core.cpp`):** The heavy lifter. A raw C++ implementation of the game rules and Minimax algorithm, exposed to Python via `pybind11`.

## 📦 Installation & Running

**Prerequisites:** Python 3.10+ (Windows Recommended for pre-built binaries)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ros-antonio/Connect4.git
    cd Connect4
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Run the Game:**
    You do **not** need to manually compile the C++ code. The script detects your OS and installs the engine automatically.
    ```bash
    python start.py
    ```
    *First run may take a few seconds to install the engine.*

## 📝 License

This project is open-source and available under the MIT License.